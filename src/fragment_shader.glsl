#version 330 core

in vec3 frag_position;
in vec3 frag_normal;
in vec2 frag_uv;

uniform float time;

uniform sampler2D colorTexture;
uniform sampler2D furTexture;
uniform int shellIndex;
uniform float alpha;

out vec4 fragColor;

vec3 light_pos = vec3(-2., 0., 2.);
float light_exp = .35;   // exposure
vec3 cube_color = vec3(.1, .0, .1);

float rand(float x) {
    return fract(sin(x) * 100);
}

void main() {
    // lighting
     vec3 n = normalize(frag_normal);
     vec3 ambient = vec3(0., 0.05, 0.);
     vec3 lightDir = normalize(light_pos);
     vec3 diffuse = vec3(max(dot(n, lightDir), 0.))/length(light_pos);

    // fur shell texturing
    vec4 texColor = texture(colorTexture, frag_uv);
    vec4 furNoise = texture(furTexture, frag_uv);
    vec3 color = (cube_color + texColor.rgb) * 0.75 + furNoise.rgb * 0.25;
    float taper = alpha - furNoise.r * shellIndex * 0.035;

    fragColor = vec4(color + ambient + diffuse * light_exp, taper);

    // debug
    vec3 random_value = vec3(rand(time));
    // fragColor = vec4(random_value, 1.0);
}
