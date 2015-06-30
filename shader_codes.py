vertex_shader_code = \
    """
    #version 430

    in layout(location=0) vec3 position;
    in layout(location=1) vec3 inColor;

    out vec3 vertexColor;

    void main()
    {
        gl_Position = vec4(position, 1.0);
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
