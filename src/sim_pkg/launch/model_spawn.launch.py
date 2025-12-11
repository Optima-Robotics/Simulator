import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from scripts import GazeboRosPaths 
from pathlib import Path
from launch.actions import TimerAction


def clean_path(raw, default=0):
  cleaned_paths = []
  for p in raw.split(':'):
    if not p.strip():
        continue  # skip empty entries
    if p.startswith('/opt/ros/humble') and not default:
        continue  # skip system ROS paths

    path_obj = Path(p)
    # If the path ends with '/..', go up one and reattach the last folder name
    if path_obj.name == '..':
        pkg_name = path_obj.parent.name  # e.g., sim_pkg
        resolved = path_obj.parent.parent / pkg_name
    else:
        resolved = path_obj.resolve()

    cleaned_paths.append(str(resolved))

  cleaned = ':'.join(cleaned_paths)
  return cleaned
 
def generate_launch_description():
 
  # Constants for paths to different files and folders
  gazebo_models_package = 'models_pkg'

  # Set the path to different files and folders.  
  pkg_model = FindPackageShare(package=gazebo_models_package).find(gazebo_models_package)

  sign_entities = {
     'crosswalk_sign': {
        'path': os.path.join(pkg_model, 'crosswalk_sign/model.sdf'),
        'coordinates': [
            (7.312, -3.240, 0.078998, 3.141592), 
            (6.627, -4.181, 0.078998, 0), 
            (6.777, -1.456, 0.078998, 3.141592),
            (6.130, -2.342, 0.078998, 0),
            (1.109,-12.486, 0.078998, 1.570796),
            (0.195,-11.869, 0.078998, 4.712388)
          ]
      },
     'enter_highway_sign': {
        'path': os.path.join(pkg_model, 'enter_highway_sign/model.sdf'),
        'coordinates': [
           (5.871,-13.970, 0.078998, 3.141592),
           (9.412, -4.850,  0.078998, 1.570796)
        ]
     },
     'leave_highway_sign': {
        'path': os.path.join(pkg_model, 'leave_highway_sign/model.sdf'),
        'coordinates': [
           (10.686, -6.276, 0.078998, 4.712388),
           (6.520, -12.700, 0.078998, 0),
           (8.458, -14.359, 0.078998, -3.15)
        ]
     },
     'oneway_sign': {
        'path': os.path.join(pkg_model, 'oneway_sign/model.sdf'),
        'coordinates': [
           (3.341, -9.821, 0.078998, 1.570796),
           (2.406, -9.821, 0.078998, 1.570796),
           (9.196,-14.375, 0.078998, 0)
        ]
     },
     'parking_sign': {
        'path': os.path.join(pkg_model, 'parking_sign/model.sdf'),
        'coordinates': [
           (4.047, -2.358, 0.078998, 0),
           (2.857, -2.358, 0.078998, 0),
           (2.779, -1.452, 0.078998, 3.141592),
           (4.459, -1.452, 0.078998, 3.141592)
        ]
     },
     'priority_sign': {
        'path':  os.path.join(pkg_model, 'priority_sign/model.sdf'),
        'coordinates': [
           (3.675,-13.050, 0.078998, 3.141592),
           (0.204, -6.031, 0.078998, 4.712388),
           (5.544,-11.381, 0.078998, 1.570796),
           (4.589, -5.997, 0.078998, 4.712388)
        ]
     },
     'prohibited_sign': {
        'path':  os.path.join(pkg_model, 'prohibited_sign/model.sdf'),
        'coordinates': [
           (3.323, -7.581, 0.078998, 4.712388),
           (2.387, -7.581, 0.078998, 4.712388),
           (11.578,-4.504, 0.078998, 4.712388)
        ]
     },
     'roundabout_sign': {
        'path':  os.path.join(pkg_model, 'roundabout_sign/model.sdf'),
        'coordinates': [
           (8.766,-4.179, 0.078998, 0),
           (10.320,-4.869,  0.078998, 1.570796),
           (11.015,-3.297,  0.078998, 3.141592)
        ]
     },
     'stop_sign': {
        'path':  os.path.join(pkg_model, 'stop_sign/model.sdf'),
        'coordinates': [
           (2.103,-14.004, 0.078998, 0),
           (4.272,-11.153, 0.078998, 3.141592),
           (0.217, -9.870, 0.078998, 4.712388),
           (1.129, -7.602, 0.078998, 1.570796),
           (12.603,-4.515, 0.078998, 1.570796),
           (4.327,-14.023, 0.078998, 0),
           (4.298, -7.342, 0.078998, 0),
           (1.423, -6.287, 0.078998, 3.141592)
        ]
     }
  }

  pedestrian_entities = {
     'pedestrian_object': {
        'path': os.path.join(pkg_model, 'pedestrian_object/model.sdf'),
        'coordinates': [
           (6.427, -1.422,  0, 3.141591),
           (1.998, -6.320,  0, 3.141591),
           (0.172,-12.200, 0, 4.712391)
        ]
     }
  }

  traffic_light_entities = {
     'traffic_light': {
        'path': os.path.join(pkg_model, 'traffic_light/model.sdf'),
        'names': ['start', 'master', 'slave', 'antimaster'],
        'coordinates': [
           (1.132,-14.403, 0, 4.712388),
           (2.030,-11.132, 0, 3.141592),
           (3.744,-10.140, 0, 0),
           (3.347,-11.483, 0, 4.712388)
        ]
     }
  }

  model_path, plugin_path, media_path = GazeboRosPaths.get_paths()
  os.environ["GAZEBO_MODEL_PATH"] = clean_path(model_path) 
   
  # Create the launch description and populate
  ld = LaunchDescription()

  # Spawn the sign objects
  for name, sign_entity in sign_entities.items():
    path = sign_entity['path']

    for i, coordinate_tuple in enumerate(sign_entity['coordinates']):
      x, y, z, Y = coordinate_tuple
      node = Node(
          package='gazebo_ros', 
          executable='spawn_entity.py',
          arguments=['-entity', name + str(i), 
                      '-file', path,
                          '-x', str(x),
                          '-y', str(y),
                          '-z', str(z),
                          '-Y', str(Y)],
                          output='screen')
      action = TimerAction(period=5.0,
                      actions=[node])
      
      ld.add_action(node)

  for name, pedestrian_entity in pedestrian_entities.items():
    path = pedestrian_entity['path']

    for i, coordinate_tuple in enumerate(pedestrian_entity['coordinates']):
      x, y, z, Y = coordinate_tuple
      sdf_args_string = f"robot_namespace:=/{name + str(i)}"
      node = Node(
          package='gazebo_ros', 
          executable='spawn_entity.py',
          arguments=['-entity', name + str(i), 
                      '-file', path,
                        '-x', str(x),
                        '-y', str(y),
                        '-z', str(z),
                        '-Y', str(Y),
                        '--ros-args', '--remap', sdf_args_string],
                        output='screen')
      
      action = TimerAction(period=5.0,
                      actions=[node])
      
      ld.add_action(action)

  for name, traffic_entity in traffic_light_entities.items():
    path = traffic_entity['path']

    for name, coordinate_tuple in zip(traffic_entity['names'], traffic_entity['coordinates']):
      x, y, z, Y = coordinate_tuple
      sdf_args_string = f"robot_namespace:=/{name}"

      node = Node(
          package='gazebo_ros', 
          executable='spawn_entity.py',
          arguments=['-entity', name, 
                      '-file', path,
                          '-x', str(x),
                          '-y', str(y),
                          '-z', str(z),
                          '-Y', str(Y),
                        '--ros-args', '--remap', sdf_args_string],
                          output='screen')
      
      action = TimerAction(period=5.0,
                      actions=[node])
      
      ld.add_action(action)

  return ld