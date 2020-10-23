import json

BER = 0.001


class Traffic:
    def __init__(self,  traffic_path, parent, *args, **kwargs) -> None:

        self.parent = parent

        print('Request Traffic Intensities:', end=' ')

        self.traffics = []

        with open(traffic_path) as traffic_file:
            traffic_info = json.load(traffic_file)

            for rate in traffic_info["Rates"]:
                self.traffics.append(rate)

                print(f"{rate:.2e} ", end="")
            print()