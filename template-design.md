### Template Design Pattern (component>Base>Content)

#### compenents: 
    - contains a component item based on user state to be used within a `<section>` in the base
#### base:  
    - holds static data, make use of state-driven component(s) and makes room for response data: >>  calls component
#### properties(eg: home.html): 
    - serves it to the user >> inherits staic data from base

Think about it in this manner: 
    - component goes into base
    - base goes into content
    - content serves the client