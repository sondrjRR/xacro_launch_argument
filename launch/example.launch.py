
import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription, actions
from launch_ros.actions import Node


def generate_launch_description():

    launch_arg_name_space = actions.DeclareLaunchArgument('name_space', default_value=''),

    # name_space = ''  # Variable we would like to adjust as a an argument for the launch file:
    name_space = launch_arg_name_space
    # I.e ros2 launch xacro_launch_argument example.launch.py --namespace 'new_namespace'
    package_name = 'xacro_launch_argument'
    package_path = os.path.join(get_package_share_directory(package_name))

    xacro_path = os.path.join(package_path, 'urdf', 'example.urdf.xacro')
    doc = xacro.process_file(xacro_path, mappings={'ns_namespace': name_space})
    robot_params = {'robot_description': doc.toxml()}

    print("-----------------------------------------------------------------------------------------------------------")
    print("xacro file path: {}".format(xacro_path))
    print("-----------------------------------------------------------------------------------------------------------")
    print(f"Name space: {name_space}")
    print("-----------------------------------------------------------------------------------------------------------")
    print(doc.toxml())
    print("-----------------------------------------------------------------------------------------------------------")

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        namespace=name_space,
        output='screen',
        parameters=[robot_params],
    )

    if name_space != '':
        name_space = name_space+'_'
    static_tf = Node(package='tf2_ros',
                     executable='static_transform_publisher',
                     name='static_transform_publisher',
                     output='log',
                     arguments=['1.0', '0', '0.55', '0.0', '0.0', '0.0', 'world', name_space+'odom'])

    return LaunchDescription([
        node_robot_state_publisher,
        static_tf,

    ])
