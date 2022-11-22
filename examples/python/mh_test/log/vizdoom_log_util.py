
def get_state_log(state):
    log = {}
    log["objects"] = get_objects_log(state.objects)
    log["labels"] = get_labels_log(state.labels)
    return log

def get_object_log(object):
    log = {}
    log['id'] = object.id
    log['name'] = object.name
    log['lx'] = object.position_x
    log['ly'] = object.position_y
    log['lz'] = object.position_z
    log['angle'] = object.angle
    log['roll'] = object.roll
    log['pitch'] = object.pitch
    log['vx'] = object.velocity_x
    log['vy'] = object.velocity_y
    log['vz'] = object.velocity_z
    return log

def get_objects_log(objects):
    log = []
    for object in objects:
        log.append(get_object_log(object))

    return log
    

def get_label_log(label):
    log = {}
    log['id'] = label.object_id
    log['x'] = label.x
    log['y'] = label.y
    log['w'] = label.width
    log['h'] = label.height
    return log

def get_labels_log(labels):
    log = []
    for label in labels:
        log.append(get_label_log(label))
    return log

