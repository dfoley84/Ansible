set_hostname:
    network.system:
        - enabled: True
        - hostname: Salt
        - apply_hostname: True
        - retain_settings: True 