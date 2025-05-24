#version 330 core

layout(location=0) in vec3 in_position;
layout(location=1) in vec3 in_normal;
layout(location=2) in vec2 in_uv;

uniform float time;

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
vec3 wind_force = vec3(.0005, 0., 0.);

float rand(float x) {
    return fract(sin(x) * 10.0);
}

void main() {
    vec3 n = normalize(in_normal);
    vec3 p = in_position + n * shellOffset * shellIndex;    // shell texturing

    // apply gravity and wind
    float influence = pow(float(shellIndex), 3.0) * 0.001;  // larger effect at the ends
    vec3 pull = gravity_force * influence;
    vec3 wind = sin(time * 2.0) * wind_force * influence;
    vec4 forces = inverse(model) * vec4(pull + wind, 1.0);
    p = p + forces.xyz;

    gl_Position = projection * view * model * vec4(p, 1.0);

    frag_position = gl_Position.xyz;
    frag_normal = mat3(transpose(inverse(model))) * in_normal + forces.xyz;
    frag_uv = in_uv;
}
