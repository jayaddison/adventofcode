content = open("16.txt").read()

def parse_line(line):
    definition_segment, link_segment = line.split(";", 1)
    name, rate_segment = definition_segment[6:].split(" ", 1)
    rate = int(rate_segment[14:])
    links = link_segment[24:].split(", ")
    return name, rate, links


assert parse_line("Valve FF has flow rate=0; tunnels lead to valves EE, GG") == (
    "FF",
    0,
    ["EE", "GG"],
)
