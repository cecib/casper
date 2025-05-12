#version 330 core

layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;

out vec3 frag_position;
out vec3 frag_normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * model * vec4(in_position, 1.0);
    frag_position = vec3(model * vec4(in_position, 1.0));
    frag_normal = mat3(transpose(inverse(model))) * in_normal;
}