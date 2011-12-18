import room
import json
from serializable import Serializable

class RoomDeSerializer(json.JSONDecoder):
    def __init__(self):
        super(RoomDeSerializer, self).__init__(object_hook=self.object_callback)

    def object_callback(self,o):
        newObj = eval('room.' + o["__jsonclass__"] + '()')

        for key in o:
            if key == "__jsonclass__":
                continue
            print key,o[key]
            newObj.__setattr__(key,o[key])

        return newObj

class RoomSerializer(json.JSONEncoder):
    def encode(self,o):
        if not isinstance(o, room.Room):
            raise TypeError("This serializer only serializes rooms.")

        # Add json class hinting
        vars_dict = vars(o)
        vars_dict["__jsonclass__"] = "Room"

        output = super(RoomSerializer,self).encode(vars_dict)
        return output

    def default(self, o):
        if isinstance(o,Serializable):
            summary = vars(o)
            summary["__jsonclass__"] = o.__class__.__name__
            return summary
        else:
            return None
            
if __name__ == "__main__":
    gameroom = room.Room(10,10)
    rs = RoomSerializer()
    gameroom.lasers.append(room.Laser((10,10)))
    gameroom.lasers.append(room.Laser((10,10)))
    gameroom.boxes.append(room.Box((10,10),30,30))
    serialized = rs.encode(gameroom)
    print serialized
    print "Serialization complete\n\n\n\n"
    rds = RoomDeSerializer()
    des = rds.decode(serialized)
    print vars(des)