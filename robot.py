print("Hello ! I am your treasure-hunt robot 🤖 ")
print("Let's find the treasure together 🪙")# The map: each room lists the rooms you can walk to next.
map_rooms = {
    "A": ["B", "C"],   # from A you can go to B or C
    "B": ["D"],        # from B you can go to D
    "C": ["D"],        # from C you can go to D
    "D": ["G"],        # from D you can go to G
    "G": [],           # G is the treasure! No need to go further.
}

print("Our map:")
print("            A  (Start)")
print("           / \\")
print("          B   C")
print("           \\ /")
print("            D")
print("            -")
print("            G  (Treasure 💎)")
print()
print("Doors from each room:", map_rooms)
def bfs(start,goal):
    to_do=[start]
    visited=[]
    order=[]

    while to_do:
        room=to_do.pop(0)

        if room in visited:
            continue
        visited.append(room)
        order.append(room)

        if room==goal:
            return order
        
        for nxt in map_rooms[room]:
            to_do.append(nxt)
    return order
order=bfs("A","G")
print("bfs checked the rooms in this order:",order)
print("number of rooms bfs checked:",len(order))
def dfs(start,goal):
    to_do=[start]
    visited=[]
    order=[]

    while to_do:
        room=to_do.pop()

        if room in visited:
            continue
        visited.append(room)
        order.append(room)

        if room==goal:
            return order
        
        for nxt in map_rooms[room]:
            to_do.append(nxt)
    return order
order=dfs("A","G")
print("dfs checked the rooms in this order:",order)
print("number of rooms dfs checked:",len(order))