#! /usr/bin/env python3

import unittest
from security_routing import *
from pathlib import Path


class TestSecurityRouting(unittest.TestCase):
    def test_example(self):
        print("\n=== Example test ===")

        stations = [
            Clearance.NONE,
            Clearance.NONE,
            Clearance.NONE,
            Clearance.NONE,
            Clearance.NONE,
            Clearance.NONE,
            Clearance.GREEN,
            Clearance.RED,
            Clearance.BLUE,
        ]
        segments = [
            (0, 2, 3, Clearance.NONE),
            (0, 3, 1, Clearance.NONE),
            (0, 5, 3, Clearance.NONE),
            (0, 6, 4, Clearance.NONE),
            (1, 4, 3, Clearance.BLUE),
            (2, 0, 3, Clearance.NONE),
            (2, 4, 3, Clearance.GREEN),
            (3, 0, 4, Clearance.NONE),
            (3, 4, 4, Clearance.NONE),
            (4, 1, 3, Clearance.BLUE),
            (4, 2, 3, Clearance.GREEN),
            (4, 3, 4, Clearance.NONE),
            (4, 7, 2, Clearance.GREEN),
            (5, 0, 3, Clearance.NONE),
            (5, 8, 4, Clearance.RED),
            (6, 0, 4, Clearance.NONE),
            (6, 8, 1, Clearance.RED),
            (7, 4, 2, Clearance.NONE),
            (8, 0, 1, Clearance.NONE)
        ]
        source = 0
        target = 1
        expected = 39

        print(f"Source station: {source}")
        print(f"Target station: {target}")
        print(f"Stations ({len(stations)}): {stations}")
        print(f"Segments ({len(segments)}):")
        for s in segments:
            print("  ", s)

        received = security_route(stations, segments, source, target)

        print(f"Expected result: {expected}")
        print(f"Received result: {received}")

        self.assertEqual(received, expected)

    @staticmethod
    def __read_problem(path):
        with open(path) as fp:
            expected = int(fp.readline())
            source = int(fp.readline())
            target = int(fp.readline())
            num_stations = int(fp.readline())
            stations = []
            for _ in range(num_stations):
                stations.append(Clearance[fp.readline().strip()])
            num_segments = int(fp.readline())
            segments = []
            for _ in range(num_segments):
                u, v, t, c = fp.readline().strip().split()
                segments.append((int(u), int(v), int(t), Clearance[c]))
        return stations, segments, source, target, expected

    def test_randoms(self):
        
        cases_dir = Path(˘BFGV CBF
        )

        for case_file in cases_dir.iterdir():
            print(f"\n=== Testing file: {case_file.name} ===")

            stations, segments, source, target, expected = self.__read_problem(case_file)

            print(f"Source: {source}, Target: {target}")
            print(f"Stations ({len(stations)}): {stations}")
            print(f"Segments ({len(segments)}): first 10 shown")
            for s in segments[:10]:
                print("  ", s)

            received = security_route(stations, segments, source, target)

            print(f"Expected: {expected}")
            print(f"Received: {received}")

            msg = f'failed test case {case_file.name}'
            self.assertEqual(received, expected, msg=msg)


if __name__ == '__main__':
    unittest.main()
