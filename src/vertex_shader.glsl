#version 330 core

layout(location=0) in vec3 in_position;
layout(location=1) in vec3 in_normal;
layout(location=2) in vec2 in_uv;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform float alpha;
uniform float shellOffset;
uniform int numShells;
uniform int shellIndex;

out vec3 frag_position;
out vec3 frag_normal;
out vec2 frag_uv;

vec3 gravity_force = vec3(0., -0.001, 0.);

void main() {
    vec3 n = normalize(in_normal);
    vec3 p = in_position + n * shellOffset * shellIndex;
    vec3 pull = gravity_force * pow(float(shellIndex), 3.0) * 0.001;
    vec4 gravity = inverse(model) * vec4(pull, 1.0);
    p = p + gravity.xyz;

    gl_Position = projection * view * model * vec4(p, 1.0);

    frag_position = gl_Position.xyz;
    frag_normal = mat3(transpose(inverse(model))) * in_normal + gravity.xyz;
    frag_uv = in_uv;
}
