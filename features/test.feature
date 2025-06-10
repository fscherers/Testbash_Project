Feature: Verificar saúde do servidor remoto

  Scenario: Servidor está com status saudável
    Given I connect via SSH to host "192.168.58.85" port 22 with username "xerao" and password "admin"
    When I check disk usage
    And I check nginx service status
    # And I check system time sync
    Then the server should be healthy
