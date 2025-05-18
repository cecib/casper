#version 330 core

in vec3 frag_position;
in vec3 frag_normal;
in vec2 frag_uv;

uniform sampler2D textureSampler;
uniform sampler2D furTexture;
uniform int shellIndex;
uniform float alpha;

out vec4 fragColor;

vec3 light_pos = vec3(-1.0, -0.5, 0.2);
float light_exp = 1.;   // exposure

void main() {
    // lighting
     vec3 n = normalize(frag_normal);
     vec3 ambient = vec3(0.1, 0.2, 0.2);
     vec3 lightDir = normalize(light_pos-frag_position);
     vec3 diffuse = vec3(max(dot(n, lightDir), 0.))/length(light_pos);

    // fur shell texturing
    vec4 texColor = texture(textureSampler, frag_uv) + vec4(-.2, .1, -.2, 1.0);
    vec4 furNoise = texture(furTexture, frag_uv);
    vec3 finalColor = texColor.rgb * 0.75 + furNoise.rgb * 0.25;

    fragColor = vec4(finalColor + diffuse * 2.0, alpha);
}
