#version 330 core

in vec3 frag_position;
in vec3 frag_normal;

out vec4 fragColor;

void main() {

    // lighting
    vec3 ambient = 0.2 * vec3(1.0, 0.0, 1.0);
    vec3 norm = normalize(frag_normal);
    vec3 lightDir = normalize(vec3(-1.0, -1.0, 0.0)-frag_position);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * vec3(1.0, 0.0, 1.0);

    fragColor = vec4(ambient + diffuse, 1.0);
}