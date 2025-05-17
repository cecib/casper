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

void main() {
    vec3 n = normalize(in_normal);
    vec3 p = in_position + n * shellOffset * shellIndex;
    gl_Position = projection * view * model * vec4(p, 1.0);

    frag_normal = mat3(transpose(inverse(model))) * in_normal;
    frag_uv = in_uv;
}
