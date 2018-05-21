Feature: Workshop Products

    Scenario: User add a product
        Given the catogory "retouches" exists, as a user
        When I add a product and selects this category
        Then the total of products is "1"
        And its category is "retouches"
        







