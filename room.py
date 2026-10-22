room = ["D","C","D","D","C"]
def show_room():
    picture = ""
    for spot in room:
        if spot == "D":
            picture += " 💩 "
        else :
            picture += " ✨ "
    print(picture) 
print("our room right now :")    
show_room()
def clean_spot(spot):
    if spot == "D":
        print("Cleaning the spot...")
        return "C"
    else:
        print("This spot is already clean!")
        return "C"
result = clean_spot("D")
print("The robot looked at a dirty spot 💩 and made it :" ,result)
print("Before the dirty room:")
show_room()
print()
for i in range(len(room)):
    room[i] = clean_spot(room[i])
print("After cleaning spot number " , i+1 , ":")
show_room()
print()
print("After all are Done! ✨ 🤖 ✨")
show_room()
room2 = ["D","C","D","D","C"]
cleaned = 0
for i in range(len(room2)):
    if room2[i] == "D":
        room2[i] = clean_spot(room2[i])
        cleaned += 1
        room2[i] = clean_spot(room2[i])
print("The robot cleaned " , cleaned , " dirty spots . 🧹 ")
print("After cleaning all dirty spots:")
show_room()
my_room = ["D","D","C","D","D","C","D","C","D"]
print("Before cleaning my room:")
show_room()
for i in range(len(my_room)):
    if my_room[i] == "D":
        my_room[i] = clean_spot(my_room[i])
print("After cleaning my room:")
show_room()
