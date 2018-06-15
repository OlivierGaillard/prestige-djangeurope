Feature: Workshop Products

    Scenario: Vendor selects an order and makes a selling for a client
        Given a product "ensemble jaune" under category "ensemble"
        Given a client with first name "toto" and name "gaga"
        Given an order for this client with this product in state "tested" exists
        When  I select this order and sell it with an amount of "20000"
        Then  a new sell is created with amount "2000"
        And   this new sell can list this order for client named "gaga" "toto".








