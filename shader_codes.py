vertex_shader_code = \
    """
    #version 430

    in layout(location=0) vec3 position;
    in layout(location=1) vec3 inColor;

    uniform mat4 model;
    uniform mat4 view;
    uniform mat4 projection;

    out vec3 vertexColor;

    void main()
    {
        gl_Position = projection * view * model * vec4(position, 1.0);
        vertexColor = inColor;
    }
    """


fragment_shader_code = \
    """
    #version 430

    in vec3 vertexColor;

    out vec4 color;

    void main()
    {
        color = vec4(vertexColor, 1.0);
    }
    """
