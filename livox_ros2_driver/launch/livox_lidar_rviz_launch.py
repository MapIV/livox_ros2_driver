import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import EnvironmentVariable
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
import launch

################### user configure parameters for ros2 start ###################
xfer_format   = 0    # 0-Pointcloud2(PointXYZRTL), 1-customized pointcloud format
multi_topic   = 0    # 0-All LiDARs share the same topic, 1-One LiDAR one topic
data_src      = 0    # 0-lidar,1-hub
publish_freq  = 10.0 # freqency of publish,1.0,2.0,5.0,10.0,etc
output_type   = 0
frame_id      = 'mid70/livox_frame'
lvx_file_path = '/home/livox/livox_test.lvx'
cmdline_bd_code = '3GGDN2J00210771'

cur_path = os.path.split(os.path.realpath(__file__))[0] + '/'
cur_config_path = cur_path + '../config'
rviz_config_path = os.path.join(cur_config_path, 'livox_lidar.rviz')
user_config_path = os.path.join(cur_config_path, 'livox_lidar_config.json')
################### user configure parameters for ros2 end #####################

# 変更点 1: パラメータを単一の辞書として定義し直す
livox_ros2_params = {
    "xfer_format": xfer_format,
    "multi_topic": multi_topic,
    "data_src": data_src,
    "publish_freq": publish_freq,
    "output_data_type": output_type,
    "frame_id": frame_id,
    "lvx_file_path": lvx_file_path,
    "user_config_path": user_config_path,
    "cmdline_input_bd_code": cmdline_bd_code
}

def generate_launch_description():

    namespace = EnvironmentVariable('ROS_NAMESPACE')

    # 変更点 2: frame_idを動的に構築し、辞書内の値を上書きする
    # namespaceとframe_idを'/'で結合する
    livox_ros2_params['frame_id'] = PathJoinSubstitution([
        namespace, # EnvironmentVariableオブジェクト
        frame_id   # 静的文字列
    ])

    livox_driver = Node(
        package='livox_ros2_driver',
        executable='livox_ros2_driver_node',
        name='livox_lidar_publisher',
        namespace=namespace,
        remappings=[
            ('livox/lidar', 'livox/mid70/lidar'),
        ],
        output='screen',
        parameters=[livox_ros2_params]
        )

    livox_rviz = Node(
            package='rviz2',
            executable='rviz2',
            namespace=namespace,
            output='screen',
            arguments=['--display-config', rviz_config_path]
        )

    return LaunchDescription([
        livox_driver,
        livox_rviz,
        # launch.actions.RegisterEventHandler(
        #     event_handler=launch.event_handlers.OnProcessExit(
        #         target_action=livox_rviz,
        #         on_exit=[
        #             launch.actions.EmitEvent(event=launch.events.Shutdown()),
        #         ]
        #     )
        # )
    ])
