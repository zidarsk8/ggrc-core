# Modals

`modal-form.js`:
 - where the basic low level code for modals exists

## `modal-ajax.js`:
 - A big click handler - looking at data-toggle to figure out which modal to open
 - The biggest one is form - all the edit object fields
 - We apply modals controller to in this file as well
 - We are handling modal:success on modal-ajax.js as well. We navigate to a new url here.
 - Dirty checks - legacy code, can be removed
 - Adding a new type of modal - create a new handler
 - _modal_show double submit/double escape, positioning
 - Register modal hook can be used to add a special modal for a module

Each modal can have its own controller that handles actions performed by the modals

## `modals_controller.js`:

 * init() 
   - fetch_all fetches the data and template
   - fetch_data a bit complex because we could be 
   - _transient property - added to the object instance while the object is open, but removed from the modal once the modal closes
   - run form_preload on the modal (if it exists)
   - apply object params - uses the data-object-params from the link that gets set on the modal. (Example requests gets the audit id in such a way).
   - data-object-params gets added to the modal controller as the options object as well
   - calls serialize_form
   _ triggers preload

 * serialize_form():
   - gets every element and then calls set_value_for_element()

 * autocomplete
   - every input that has data-lookup defined on it
   - autocomplete_select() is what is called when the autocomplete value is selected

 * set_value():
   - keeping

## Naming conventions in the forms:
 - name of the input maps to the value of the instance. most commonly <input name='url', value='{{url}}' />
 - if name is name='contact.email' value="{{contact.email}}" - special cases for null in data-lookup onkeyup so that it clears the field

data-also set - sets the attr of value bot also of the field in



