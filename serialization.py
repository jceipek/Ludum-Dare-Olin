import room
import json

class RoomDeSerializer(json.JSONDecoder):
    def __init__(self):
        super(RoomDeSerializer, self).__init__(object_hook=self.object_callback)

    def object_callback(self,o):
        newObj = eval('Room.' + o["__jsonclass__"] + '()')

        for key in o:
            if key == "__jsonclass__":
                continue
            newObj.__setattr__(key,o[key])

        return newObj

class RoomSerializer(json.JSONEncoder):
    def encode(self,o):
        if not isinstance(o, Room.Room):
            raise TypeError("This serializer only serializes rooms.")

        # Add json class hinting
        vars_dict = vars(o)
        vars_dict["__jsonclass__"] = "Room"

        output = super(RoomSerializer,self).encode(vars_dict)
        return output

    def default(self, o):
        summary = vars(o)
        summary["__jsonclass__"] = o.__class__.__name__
        return summary

if __name__ == "__main__":
    room = room.Room(10,10)
    rs = RoomSerializer()
    room.lasers.append(Room.Laser((10,10)))
    room.lasers.append(Room.Laser((10,10)))
    serialized = rs.encode(room)
    print serialized
    print "Serialization complete\n\n\n\n"
    rds = RoomDeSerializer()
    des = rds.decode(serialized)
    print vars(des)