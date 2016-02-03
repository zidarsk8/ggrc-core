# Creating A New Mockup

1. Add a new mockup URL to `src/views/mockups.py`:

    ```
    @app.route("/mockups/new_mockup")
    @login_required
    def mockup_sample2():
      return render_template("mockups/base.haml")
    ```

    This should create a new mockup page on [http://localhost:8080/mockups/new_mockup]
    If you want to remove or add some element which is defined in
    `mockups/base.haml`, create a new haml file e.g. `mockups/new_mockup.haml`
    and fill it up with needed elements. Don't forget to change the template in
    the `render_template()` function in your view.

2. Create a new folder inside `src/ggrc/assets/mockups` named `new_mockup`.

3. Create a `main.js` inside the newly created folder and add the file under `assets.yaml` (under `mockup-js-files`).

4. `main.js` should look something like this:

    ```
    (function (can, $) {

      // Only load this file when the URL is mockups/sample:
      if (window.location.pathname !== "/mockups/new_mockup") {
        return;
      }

      // Setup the object page:
      var mockup = new CMS.Controllers.MockupHelper($('body'), {
        // Object:
        object: {
          icon: "grciconlarge-program",
          title: "New Mockup",
        },
        // Views:
        views: [{
            // Example on how to use an existing template:
            title: "Info",
            icon: "grcicon-info",
            template: "/base_objects/info.mustache",
          }
        ],
      });
    })(this.can, this.can.$);
    ```

    The main.js file should create a new instance of MockupHelper, where you
    can define the page object (currently only title/icon can be defined) and
    one or more views (tabs) that will be shown on the page.

    When defining views you can use a newly created template
    (add it to the `new_mockup` folder and to `assets.yml`
    under `mockup-js-template-files`).

    For an example on how to use mustache variables in your template and
    custom events see the sample mockup `src/assets/mockups/sample`.
