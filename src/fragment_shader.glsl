#version 330 core

in vec3 frag_position;
in vec3 frag_normal;
in vec2 frag_uv;

uniform sampler2D textureSampler;
uniform sampler2D furTexture;
uniform float alpha;

out vec4 fragColor;

vec3 light_pos = vec3(-1.0, -0.5, 0.2);
float light_exp = 1.;   // exposure

void main() {
    // vec3 n = normalize(frag_normal);
    // vec3 cube_col = vec3(0.2, 0.2, 0.2);

    // lighting
    // vec3 ambient = vec3(0.1, 0.2, 0.2)
    // vec3 lightDir = normalize(light_pos-frag_position);
    // vec3 diffuse = vec3(max(dot(n, lightDir), 0.))/length(light_pos);

    // Specular
    // float spec = pow(max(dot(view_dir, reflect_dir), 0.0), material_shininess)
    // vec3 specular = material_specular * spec * light_color

    // textures
    vec4 texColor = texture(textureSampler, frag_uv);
    vec4 furColor = texture(furTexture, frag_uv);
//    float alphaFinal = alpha - furColor.r;

//    if (alpha < 0.5) {
//        fragColor = vec4(1., .6, 1., 1.0);
//    } else {
    fragColor = vec4(furColor.rgb, 1.0);  //alphaFinal);
//    }
}
    // fragColor = vec4(texColor.xyz + light_exp * diffuse, 1.0);}

