#version 330 core

layout(location=0) in vec3 in_position;
layout(location=1) in vec3 in_normal;
layout(location=2) in vec2 in_uv;

uniform float time;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

uniform int numShells;
uniform int shellIndex;
uniform float shellOffset;
uniform float alpha;

out vec3 frag_position;
out vec3 frag_normal;
out vec2 frag_uv;

out vec3 debug_val;

vec3 gravity_force = vec3(0., -0.001, 0.);
vec3 wind_force = vec3(.0005, 0., 0.);

float rand(float t) {
    return fract(sin(t) * 356548.);
}

float rand_2(vec2 uv) {
    return fract(sin(dot(uv, vec2(12.98, 78.23))) * 356548.);
}

void main() {
    vec3 n = normalize(in_normal);
    vec3 p = in_position + n * shellOffset * shellIndex;    // shell texturing

    // apply gravity and wind
    float infl = pow(float(shellIndex), 3.0) * 0.001;   // larger effect at ends
    vec3 pull = gravity_force * infl;
    vec3 wind = (sin(time * 3. * rand_2(in_uv)) + 1.0) * wind_force * infl;
    vec4 forces = inverse(model) * vec4(pull + wind, 1.0);
    p = p + forces.xyz;

    gl_Position = projection * view * model * vec4(p, 1.0);

    frag_position = gl_Position.xyz;
    frag_normal = mat3(transpose(inverse(model))) * in_normal + forces.xyz;
    frag_uv = in_uv;

    debug_val = wind;
}
