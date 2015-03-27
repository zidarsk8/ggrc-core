# Adding a new Object

## Backend

### Create `new_object.py` in `src/<module>/models/`

```
class NewObject(mixins..., db.Model):
  __tablename__ = 'new_objects'

  new_object_attr = deferred(db.Column(db.String), 'NewObject')

  # REST properties
  _publish_attrs = [
      'new_object_attr',
  ]
```

Add the NewObject to the `all_models` list in `all_models.py`, or register it using the `register_model` method if your adding it inside a module.

### Generate a migration file

```
python src/ggrc/migrate.py <module> revision --autogenerate -m "Add NewObject"
```

Consider the generated migration file a template that you need to manually update.

**Important:** Make sure both `db_migrate` and `db_downgrade` are working correctly, both in a clean database and in a database with existing data

### Add new Object to appropriate services

1. `ggrc/cache/cache.py` # configure memcache
2. `ggrc/services/__init__.py` or use `init_extra_services()` # init REST APIs for NewObject
3. `ggrc/views/__init__.py` or use `init_extra_views()` # init object view page

### Add permissions for NewObject

Add the NewObject to appropriate roles in `ggrc_basic_permissions/roles`

## Frontend

### Create a CMS.Models.Cacheable object

```
can.Model.Cacheable("CMS.Models.NewObject", {
  root_object : "new_object",
  root_collection : "new_objects",
  findOne : "GET /api/new_objects/{id}",
  update : "PUT /api/new_objects/{id}",
  destroy : "DELETE /api/new_objects/{id}",
  create : "POST /api/new_objects",
  mixins : ["ownable", "contactable"],
  is_custom_attributable: true,
  attributes : {
    context : "CMS.Models.Context.stub",
    modified_by : "CMS.Models.Person.stub",
    custom_attribute_values : "CMS.Models.CustomAttributeValue.stubs",
    start_date: "date",
    end_date: "date"
  },
  init : function() {
    this._super && this._super.apply(this, arguments);
    this.validateNonBlank("title");
  }
}, {
  object_model: can.compute(function() {
    return CMS.Models[this.attr("object_type")];
  }),
  after_save: function() {
  }
});
```

### Add new_object to `object_type_decision_tree` in assets/javascripts/application.js

### Add new_object to `business_object.js`

`base_widgets_by_type` is where you define the attributes shown in widgets

### Add NewObject to `mappings.js`

### Add NewObject to the LHN

In `src/ggrc/assets/mustache/dashboard/lhn.mustache` add the line:

```{{{renderLive '/static/mustache/dashboard/lhn_search.mustache' type="NewObject" li_class="class"}}}```

## Create mustache files

## Mappings
