from controller import Supervisor

waypoints = [
    (0.482241, 0.161931),
    (0.421806, 0.420397),
    (0.246497, 0.478845),
    (0.246458, 0.292904),
    (0.245034, 0.637886),
    (0.246153, -0.168601),
    (0.416948, -0.273868),
    (0.246199, -0.408029),
    (0.409342, -0.490217),
    (-0.244443, -0.491632),
    (-0.478711, -0.410307),
    (-0.0308504, 0.475415),
    (-0.0313106, 0.175906),
    (0.04561, 0.0639004),
    (-0.0712083, -0.155879),
    (-0.410935, 0.417269),
    (-0.41016, -0.0454242)
]

# Create a supervisor instance
supervisor = Supervisor()

# Get the root node of the supervisor tree
root_node = supervisor.getRoot()

# Find the IndexedLineSet node by name
indexed_line_set_node = root_node.getField("line").getSFNode()

# Access the Coordinate node within the IndexedLineSet
coord_node = indexed_line_set_node.getField("coordinates").getSFNode()

# Access the points within the Coordinate node
points_field = coord_node.getField("point")

# Get the number of points
num_points = points_field.getCount()

for i in num_points:
    print(i)

while robot.step(TIME_STEP) != -1:
  


