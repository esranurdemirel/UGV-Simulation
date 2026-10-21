import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_gazebo = get_package_share_directory('marduk_gazebo')
    pkg_navigation = get_package_share_directory('marduk_navigation')
    pkg_nav2_bringup = get_package_share_directory('nav2_bringup')

    slam_config = os.path.join(pkg_navigation, 'config', 'slam_toolbox.yaml')

    # 1. Senin tıkır tıkır çalışan simülasyon launch dosyan
    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo, 'launch', 'sim.launch.py')
        )
    )

    # 2. İŞTE EKSİK OLAN VE HARİTAYI BAŞLATACAK ANA MOTOR (SLAM TOOLBOX)
    slam_toolbox = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            slam_config,
            {'use_sim_time': True} # Gazebo saatiyle senkron çalışması için şart
        ]
    )

    # 3. Nav2 Paneli ve RViz Ayarları
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2_bringup, 'launch', 'navigation_launch.py')
        ),
        launch_arguments={'use_sim_time': 'true'}.items(),
    )

    rviz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_nav2_bringup, 'launch', 'rviz_launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'true',
            'robot_base_frame': 'marduk_ika/chassis',
            'global_frame': 'map',
            'odom_frame': 'odom'
        }.items(),
    )

    return LaunchDescription([
        simulation,
        slam_toolbox,  # Eksik olan bu düğümü ROS evrenine fırlatıyoruz
        nav2,
        rviz
    ])