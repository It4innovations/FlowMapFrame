import pandas as pd

from datetime import datetime, timedelta


class Row:
    def __init__(self, row):
        self.timestamp = row[0][0]
        self.from_node_id = int(row[0][1])
        self.to_node_id = int(row[0][2])
        self.vehicle_id = int(row[1][0])
        self.start_offset_m = row[1][1]

    def __str__(self):
        # return str(f"_{self.timestamp}_, {self.from_node_id}, {self.to_node_id}, {self.vehicle_id},
        # {self.start_offset_m}")
        return str((self.timestamp, self.from_node_id, self.to_node_id, self.vehicle_id, self.start_offset_m))


class Segment:
    """Route segment"""

    def __init__(self, from_node_id, to_node_id, timestamp, vehicle_count, car_index):
        self.from_node_id = int(from_node_id)
        self.to_node_id = int(to_node_id)
        self.timestamp = timestamp
        self.vehicle_count = int(vehicle_count)
        self.density = -1
        self.car_indexes = [int(car_index)]
        self.car_offsets = []   # will be moved elswhere later

    def __str__(self):
        return str((self.from_node_id, self.to_node_id, self.timestamp, self.vehicle_count, self.car_indexes))


def load_row(rows, row_index, times):
    row = rows[row_index]

    end_time = rows[-1].timestamp
    # time before car changes segment
    for i in range(row_index + 1, len(rows)):

        if rows[i].vehicle_id == row.vehicle_id:
            end_time = rows[i].timestamp - timedelta(seconds=1)
            break

    time_range = int((end_time - row.timestamp).total_seconds())

    # add the car for every second in time_range of this row
    for i in range(0, time_range + 1):
        current_time = row.timestamp + timedelta(seconds=i)

        # the array of times is indexed from zero
        times_index = int((current_time - rows[0].timestamp).total_seconds())

        # get already recorded segments at current time:
        if len(times) <= times_index:
            times.append([])

        segments = times[times_index]
        # add row to segments
        load_row_in_time(segments, row, current_time)

    return


def load_row_in_time(segments, row, current_time):
    for segment in segments:
        if (segment.from_node_id, segment.to_node_id) == (row.from_node_id, row.to_node_id):
            segment.vehicle_count += 1
            segment.car_indexes.append(row.vehicle_id)
            segment.car_offsets.append(row.start_offset_m)
            return

    # segment not recorded at this time yet:
    segments.append(Segment(row.from_node_id, row.to_node_id, current_time, 1, row.vehicle_id))
    segments[-1].car_offsets.append(row.start_offset_m)
    return


def load_input(path):
    data = pd.read_pickle(path)

    rows = [Row(r) for r in data.iterrows()]

    times = []

    for i in range(0, len(rows)):
        load_row(rows, i, times)

    # for time in times:
    #     print('----')
    #     for segment in time:
    #         print(segment.from_node_id, segment.to_node_id, segment.timestamp, segment.vehicle_count,
    #               segment.car_indexes)
    return times
