"""Regression through the editor's actual Project.split interface; never edits sources."""
from pathlib import Path
import argparse
import json
import sys
import unittest
from collections import Counter
from datetime import datetime, timezone

W = Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
cli = argparse.ArgumentParser()
cli.add_argument('--editor', type=Path, required=True)
cli.add_argument('--source', type=Path, default=W / 'exports/resumed-integrated-20261101-a')
cli.add_argument('--roundtrip', action='store_true')
cli.add_argument('--report', type=Path)
args, rest = cli.parse_known_args()
sys.path.insert(0, str(args.editor))
from model import Project, levels, tree_manifest, clone, block, setval, emit, parse

SOURCE = args.source.resolve()
PARENT = 'STATE_EASTERN_NORWAY'
CHILD = 'STATE_EDITOR_ROUNDING_FIXTURE'
STAMP = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
OBSERVATIONS = []


def record(name, **details):
    OBSERVATIONS.append({'name': name, **details})


def logging_row(project, region=PARENT):
    return next(b for _, b in project.state_rows('buildings', region)
                if b.scalar('building') == 'building_logging_camp')


def owner_rows(building):
    return [own for add in building.all('add_ownership') for own in add.children]


def identity(own):
    region = own.scalar('region', '')
    if region == CHILD:
        region = PARENT
    return (own.key, own.scalar('country', ''), own.scalar('type', ''), region)


def investment_totals(buildings):
    result = Counter()
    for b in buildings:
        for own in owner_rows(b):
            result[identity(own)] += int(own.scalar('levels'))
    return result


class SplitRounding(unittest.TestCase):
    def test_real_two_level_logging_camp_splits_one_level_each(self):
        source_hashes = tree_manifest(SOURCE)
        project = Project(SOURCE)
        logging = next(b for _, b in project.state_rows('buildings', PARENT)
                       if b.scalar('building') == 'building_logging_camp')
        self.assertEqual([int(n.value) for n in logging.walk() if n.key == 'levels'], [1, 1])
        before = project.totals()
        original = clone(logging)
        project.split(PARENT, CHILD, ['X01EB0A'])
        def logging_levels(region):
            return sum(levels(b) for _, b in project.state_rows('buildings', region)
                       if b.scalar('building') == 'building_logging_camp')
        observed = {'parent': logging_levels(PARENT), 'child': logging_levels(CHILD),
                    'totals_conserved': before == project.totals()}
        print(json.dumps(observed), flush=True)
        self.assertEqual(observed, {'parent': 1, 'child': 1, 'totals_conserved': True})
        parent, child = logging_row(project), logging_row(project, CHILD)
        self.assertEqual(investment_totals([parent, child]), investment_totals([original]))
        for b in [parent, child]:
            self.assertEqual(b.get('activate_production_methods').values(), original.get('activate_production_methods').values())
            self.assertTrue(all(int(own.scalar('levels')) > 0 for own in owner_rows(b)))
        self.assertEqual(owner_rows(child)[0].scalar('region'), CHILD)
        self.assertEqual(owner_rows(parent)[0].scalar('region'), PARENT)
        self.assertIsNot(parent, child)
        self.assertIsNot(owner_rows(parent)[0], owner_rows(child)[0])
        self.assertEqual(tree_manifest(SOURCE), source_hashes)
        record('real_two_level_logging_camp', **observed, owner_totals_preserved=True, production_methods_preserved=True)

    def test_odd_levels_and_explicit_ratios_use_whole_building_total(self):
        for amount, ratio, expected_parent, expected_child in [(3, .5, 2, 1), (10, .1, 9, 1), (10, .99, 1, 9)]:
            with self.subTest(levels=amount, ratio=ratio):
                project = Project(SOURCE)
                index = next(i for i, (_, b) in enumerate(project.state_rows('buildings', PARENT))
                             if b.scalar('building') == 'building_logging_camp')
                project.building_levels_set(PARENT, index, amount)
                original = clone(logging_row(project))
                totals = project.totals()
                project.split(PARENT, CHILD, ['X01EB0A'], ratio)
                old, new = logging_row(project), logging_row(project, CHILD)
                self.assertEqual((levels(old), levels(new)), (expected_parent, expected_child))
                self.assertEqual(investment_totals([old, new]), investment_totals([original]))
                self.assertEqual(project.totals(), totals)
                record('explicit_ratio', levels=amount, ratio=ratio, parent=levels(old), child=levels(new))

    def test_repeated_foreign_investors_keep_identity_order_and_both_objects(self):
        project = Project(SOURCE)
        logging = logging_row(project)
        foreign = clone(owner_rows(logging)[0])
        setval(foreign, 'country', '"c:SWE"')
        setval(foreign, 'region', '"STATE_SVEALAND"')
        setval(foreign, 'levels', 2)
        local = clone(owner_rows(logging)[1])
        setval(local, 'levels', 2)
        logging.children = [n for n in logging.children if n.key != 'add_ownership']
        logging.children += [block('add_ownership', [foreign, clone(foreign)]), block('add_ownership', [local])]
        original = clone(logging)
        total = project.totals()
        project.split(PARENT, CHILD, ['X01EB0A'])
        old, new = logging_row(project), logging_row(project, CHILD)
        self.assertEqual((levels(old), levels(new)), (3, 3))
        for b in [old, new]:
            self.assertEqual([len(add.children) for add in b.all('add_ownership')], [2, 1])
            self.assertEqual([int(own.scalar('levels')) for own in owner_rows(b)], [1, 1, 1])
            self.assertEqual([identity(own) for own in owner_rows(b)], [identity(own) for own in owner_rows(original)])
            self.assertEqual([own.scalar('region') for own in owner_rows(b)[:2]], ['STATE_SVEALAND', 'STATE_SVEALAND'])
            self.assertEqual(b.get('activate_production_methods').values(), original.get('activate_production_methods').values())
        self.assertEqual(owner_rows(new)[2].scalar('region'), CHILD)
        self.assertEqual(owner_rows(old)[2].scalar('region'), PARENT)
        self.assertEqual(investment_totals([old, new]), investment_totals([original]))
        self.assertEqual(project.totals(), total)
        for a, b in zip(owner_rows(old), owner_rows(new)):
            self.assertIsNot(a, b)
        record('repeated_foreign_investors', duplicate_ownership_blocks_preserved=True,
               foreign_reference='c:SWE/STATE_SVEALAND', local_new_reference=CHILD, parent=3, child=3)

    def test_zero_child_is_filtered_without_removing_parent_owner(self):
        project = Project(SOURCE)
        index = next(i for i, (_, b) in enumerate(project.state_rows('buildings', PARENT))
                     if b.scalar('building') == 'building_logging_camp')
        project.building_levels_set(PARENT, index, 1)
        original = clone(logging_row(project))
        total = project.totals()
        project.split(PARENT, CHILD, ['X01EB0A'])
        self.assertEqual(levels(logging_row(project)), 1)
        self.assertFalse(any(b.scalar('building') == 'building_logging_camp' for _, b in project.state_rows('buildings', CHILD)))
        self.assertEqual(investment_totals([logging_row(project)]), +investment_totals([original]))
        self.assertEqual(project.totals(), total)
        record('zero_child_filtered', parent=1, child=0, owner_preserved=True)

    def test_complete_country_intersection_moves_all_its_buildings(self):
        project = Project(SOURCE)
        source = 'STATE_DOBRUDJA'
        selected = project.owners[source]['TUR']
        original = [clone(b) for tag, b in project.state_rows('buildings', source) if tag == 'TUR']
        self.assertTrue(original)
        total = project.totals()
        project.split(source, CHILD, selected, .5)
        moved = [b for tag, b in project.state_rows('buildings', CHILD) if tag == 'TUR']
        self.assertFalse(any(tag == 'TUR' for tag, _ in project.state_rows('buildings', source)))
        self.assertEqual([levels(b) for b in moved], [levels(b) for b in original])
        self.assertEqual([b.scalar('building') for b in moved], [b.scalar('building') for b in original])
        self.assertEqual(project.totals(), total)
        record('complete_owner_intersection', region=source, moved_building_count=len(moved), moved_levels=sum(levels(b) for b in moved))

    @unittest.skipUnless(args.roundtrip, 'Enable explicit external roundtrip fixtures')
    def test_corrected_split_project_save_reopen_and_incomplete_export_rejection(self):
        project = Project(SOURCE)
        source_hashes = tree_manifest(SOURCE)
        project.split(PARENT, CHILD, ['X01EB0A'])
        path = W / 'projects' / ('editor-rounding-split-' + STAMP + '.json')
        project.save_project(path)
        restored = Project.load_project(path)
        self.assertEqual(restored.totals(), project.totals())
        self.assertEqual(emit(logging_row(restored)), emit(logging_row(project)))
        self.assertEqual(emit(logging_row(restored, CHILD)), emit(logging_row(project, CHILD)))
        for document in restored.docs.values():
            parse(document.render())
        destination = W / 'exports' / ('editor-rounding-incomplete-' + STAMP)
        with self.assertRaisesRegex(ValueError, 'choose .*hub|missing .*locator|port buildings need'):
            restored.export(destination)
        self.assertFalse(destination.exists())
        self.assertEqual(tree_manifest(SOURCE), source_hashes)
        record('split_save_reopen', project=str(path), loaded_source=str(restored.mod),
               parent=levels(logging_row(restored)), child=levels(logging_row(restored, CHILD)),
               incomplete_geometry_export_rejected=True)

    @unittest.skipUnless(args.roundtrip, 'Enable explicit external roundtrip fixtures')
    def test_current_source_no_action_save_reopen_export_keeps_game_data(self):
        project = Project(SOURCE)
        source_hashes = tree_manifest(SOURCE)
        path = W / 'projects' / ('editor-rounding-noaction-' + STAMP + '.json')
        project.save_project(path)
        self.assertEqual(json.loads(path.read_text(encoding='utf8'))['files'], {})
        restored = Project.load_project(path)
        self.assertEqual(restored.totals(), project.totals())
        self.assertEqual(tree_manifest(restored.mod), source_hashes)
        destination = W / 'exports' / ('editor-rounding-noaction-' + STAMP)
        review = restored.export(destination)
        self.assertEqual(review['changed_files'], [])
        self.assertFalse(review['engine_verified'])
        exported_hashes = tree_manifest(destination)
        for rel, digest in source_hashes.items():
            if rel != '.metadata/metadata.json':
                self.assertEqual(exported_hashes[rel], digest, rel)
        self.assertEqual(tree_manifest(Path(review['candidate_backup']) / 'mod'), exported_hashes)
        self.assertEqual(tree_manifest(SOURCE), source_hashes)
        reopened = Project(destination)
        self.assertEqual(reopened.totals(), project.totals())
        self.assertEqual([emit(b) for _, b in reopened.state_rows('buildings', PARENT)],
                         [emit(b) for _, b in project.state_rows('buildings', PARENT)])
        record('noaction_save_reopen_export', project=str(path), export=str(destination),
               candidate_backup=review['candidate_backup'], game_files_unchanged=True, changed_files=review['changed_files'])


if __name__ == '__main__':
    before = tree_manifest(SOURCE)
    result = unittest.main(argv=[sys.argv[0], *rest], exit=False).result
    unchanged = tree_manifest(SOURCE) == before
    if args.report:
        args.report.write_text(json.dumps({'source': str(SOURCE), 'source_manifest': before,
            'editor': str(args.editor), 'editor_manifest': tree_manifest(args.editor),
            'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors),
            'skipped': len(result.skipped), 'source_unchanged': unchanged, 'observations': OBSERVATIONS,
            'engine_verified': False, 'game_launched': False}, ensure_ascii=False, indent=2), encoding='utf8')
    sys.exit(0 if result.wasSuccessful() and unchanged else 1)
