import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_gazebo = get_package_share_directory('marduk_gazebo')
    pkg_description = get_package_share_directory('marduk_description')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Senin dünyandaki robot.world dosyasının tam yolu
    # (Eğer dosyan direkt 'worlds' klasörünün içindeyse burayı 'worlds', 'robot.world' yapabilirsin)
    world_file = os.path.join(pkg_gazebo, 'worlds', 'robot.world')
    bridge_config = os.path.join(pkg_gazebo, 'config', 'ros_gz_bridge.yaml')

    # 1. Gazebo Simülasyonu Başlatıcı
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r {world_file}'}.items(),
    )

    # 2. Robot State Publisher Çağırıcısı (Diğer paketten çekiyoruz)
    robot_state_pub = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_description, 'launch', 'description.launch.py')
        )
    )

    # 3. Gelişmiş YAML Destekli ROS-Gazebo Köprüsü
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        output='screen',
        parameters=[{
            'config_file': bridge_config,
            'use_sim_time': True
        }]
    )

    return LaunchDescription([
        gazebo,
        robot_state_pub,
        bridge
    ])