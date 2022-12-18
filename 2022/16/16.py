content = open("16.txt").read()

def parse_line(line):
    definition_segment, link_segment = line.split(";", 1)
    name, rate_segment = definition_segment[6:].split(" ", 1)
    rate = int(rate_segment[14:])
    link_words = link_segment.split(" ")
    links = "".join(link_words[5:]).split(",")
    return name, rate, links


assert parse_line("Valve FF has flow rate=0; tunnels lead to valves EE, GG") == (
    "FF",
    0,
    ["EE", "GG"],
)

assert parse_line("Valve TT has flow rate=99; tunnel leads to valve TT") == (
    "TT",
    99,
    ["TT"],
)
