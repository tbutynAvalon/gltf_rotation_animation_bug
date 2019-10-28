import base64
import struct
import json


FLOAT_STRIDE = 4
UNSIGNED_SHORT_STRIDE = 2
def look_at_gltf(buffers):
    buffer_offset = 0
    buffer_views = []
    for i in zip(byte_lengths, unpack_type, values_per_entry):
        single_buffer_view = []
        buf = buffers[buffer_offset:buffer_offset+i[0]]
        buffer_offset += i[0]
        vec = []
        if i[1] == 'f':
            stride = FLOAT_STRIDE
        if i[1] == 'H':
            stride = UNSIGNED_SHORT_STRIDE
        for j in range(0, i[0], stride):
            vec.append(struct.unpack(i[1], buf[j:j+stride]))
            if (j / stride + 1) % i[2] == 0:
                single_buffer_view.append(vec)
                vec = []
        buffer_views.append(single_buffer_view)
    return buffer_views

json_file = open("NoYRotation.gltf")
json_str = json_file.read()
json_data = json.loads(json_str)
buffer_str = json_data['buffers'][0]['uri']
real_buffer_index = buffer_str.find('base64') + len('base64') + 1
buffer_str = buffer_str[real_buffer_index:]
buffers_scale_0_1 = bytearray(base64.standard_b64decode(buffer_str))

json_file = open("YRotation.gltf")
json_str = json_file.read()
json_data = json.loads(json_str)
buffer_str = json_data['buffers'][0]['uri']
real_buffer_index = buffer_str.find('base64') + len('base64') + 1
buffer_str = buffer_str[real_buffer_index:]
buffers_scale_1_0 = bytearray(base64.standard_b64decode(buffer_str))

# I didn't want to write a full gltf parser so I just used the values directly with the aid of a text viewer.
byte_lengths = [288, 288, 192, 72, 12, 48]
# f = float, H = unsigned shortd
unpack_type = ['f', 'f', 'f', 'H', 'f', 'f']
# 3 = VEC3, 2 = VEC2, 1 = Scalar
values_per_entry = [3, 3, 2, 1, 1, 3]

buffer_views1_0 = look_at_gltf(buffers_scale_1_0)
buffer_views0_1 = look_at_gltf(buffers_scale_0_1)

not_equal = []
for i in range(len(buffer_views0_1)):
    compare_results_layer0 = []
    for j in range(len(buffer_views0_1[i])):
        compare_results_layer1 = []
        if isinstance(buffer_views0_1[i][j], list):
            compare_results_layer2 = []
            for k in range(len(buffer_views0_1[i][j])):
                if buffer_views0_1[i][j][k] != buffer_views1_0[i][j][k]:
                    not_equal.append((i, j, k, buffer_views0_1[i][j][k][0], buffer_views1_0[i][j][k][0], buffer_views0_1[i][j][k][0] - buffer_views1_0[i][j][k][0]))

if(len(not_equal) > 0):
    print("Good! Modifying the scale of the right control point modified the following values: \n {}".format(not_equal))
else:
    print("Error no values were changed even though the Y rotation was adjusted to be non-zero")
