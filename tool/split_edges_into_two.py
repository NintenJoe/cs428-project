import json

name = "boss"
json_data = open(name + ".json")
data = json.load(json_data)

f = open(name + "2.json", "w")

new_states = []
for edge in data["edges"]:
    new_hit_state = edge[0] + "_" + edge[1]
    new_regex = ".*'victim': boss.*"
    new_state1 = "[\n    \"" + str(edge[0]) + "\",\n    \"hit_" + str(new_hit_state) + "\",\n    \"" + new_regex + "\"\n],\n"
    new_state2 = "[\n    \"hit_" + new_hit_state + "\",\n    \"" + str(edge[1]) + "\",\n    \"" + new_regex + "\"\n],\n"
    f.write(new_state1)
    f.write(new_state2)

    new_states.append(new_hit_state)

for state in new_states:
    state_str = "[\n    \"HitState.HitState\",\n    \"" + state.encode("ascii") + "\",\n    " + str(1) + "\n],\n"
    f.write(state_str)

f.close()