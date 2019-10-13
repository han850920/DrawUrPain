Group_list ={
        'blue':[list() for i in range(10)],
        'green':[list() for i in range(10)],
        'orange':[list() for i in range(10)],
        'red':[list() for i in range(10)],
        'cyan':[list() for i in range(10)],
        'pink':[list() for i in range(10)]
    }
Group_list['pink'][3].append([(3,5)])
Group_list['pink'][3][0].append((4,7))

Group_list['pink'][3].append([(9,4)])
print(len(Group_list['pink'][3]))