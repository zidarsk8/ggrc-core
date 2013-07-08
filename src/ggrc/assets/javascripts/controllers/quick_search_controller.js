/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//require can.jquery-all

(function(can, $) {
  function with_params(href, params) {
    if (href.charAt(href.length - 1) === '?')
      return href + params;
    else if (href.indexOf('?') > 0)
      return href + '&' + params;
    else
      return href + '?' + params;
  }

  function get_attr(el, attrnames) {
    var attrval = null
    , $el = $(el);
    can.each(can.makeArray(attrnames), function(attrname) {
      var a = $el.attr(attrname);
      if(a) {
        attrval = a;
        return false;
      }
    });
    return attrval;
  }

CMS.Controllers.Filterable("CMS.Controllers.QuickSearch", {
  defaults : {
    list_view : GGRC.mustache_path + "/dashboard/object_list.mustache"
    , tooltip_view : GGRC.mustache_path + "/dashboard/object_tooltip.mustache"
    , spin : true
    , tab_selector : 'ul.nav-tabs:first > li > a'
    , tab_href_attr : [ "href", "data-tab-href" ]
    , tab_target_attr : [ "data-tab-target", "href" ]
    , tab_model_attr : [ "data-model", "data-object-singular" ]
    , limit : null
  }
}, {

  setup : function(el, opts) {
    this._super && this._super.apply(this, arguments);
    if(!opts.observer) {
      opts.observer = new can.Observe();
    }
  }

  , init : function(opts) {
    var that = this;
    var $tabs = this.element.find(this.options.tab_selector);
    $tabs.each(function(i, tab) {
      var $tab = $(tab)
      , href = get_attr($tab, that.options.tab_href_attr)
      , loaded = $tab.data('tab-loaded')
      , pane = get_attr($tab, that.options.tab_target_attr)
      , $pane = $(pane)
      , template = $tab.data("template") || that.options.list_view
      , model_name = get_attr($tab, that.options.tab_model_attr)
      , model = can.getObject("CMS.Models." + model_name) || can.getObject("GGRC.Models." + model_name)
      , view_data = null
      , spinner;

      if(!template && typeof console !== "undefined") {
        console.warn("No template defined for quick_search in ", $pane.attr("id"));
      }

      if(model && template) {
        view_data = new can.Observe({
          list: new model.List()
          , all_items: new model.List()
          , filtered_items: new model.List()
          , observer: that.options.observer
          , tooltip_view : that.options.tooltip_view
          , model : model
        });

        $tab.data("view_data", view_data);
        $tab.data("model", model);
        model.findAll().done(function(data) {
          view_data.attr('all_items', data);
          view_data.attr('filtered_items', data.slice(0));
          if($tab.is("li.active a")) {
            can.Observe.startBatch();
            if(that.options.limit != null) {
              view_data.attr('list').replace(data.slice(0, that.options.limit));
            } else {
              view_data.attr('list', data);
            }
            can.Observe.stopBatch();
          } else {
            GGRC.queue_event(function() {
              if(that.options.limit != null) {
                view_data.attr('list').replace(data.slice(0, that.options.limit));
              } else {
                view_data.attr('list', data);
              }
            });
          }
          $tab.find(".item-count").html(data ? data.length : 0);
        });

        model.bind("created", function(ev, instance) {
          if(instance.constructor === model) {
            view_data.list.unshift(instance.serialize());
          }
        });
      }

      if(that.options.spin) {
        spinner = new Spinner({ }).spin();
        $pane.html(spinner.el);
        // Scroll up so spinner doesn't get pushed out of visibility
        $pane.scrollTop(0);
        $(spinner.el).css({ width: '100px', height: '100px', left: '50px', top: '50px', zIndex : calculate_spinner_z_index });
      }

      if (view_data) {
        can.view(template, view_data, function(frag, xhr) {
          $tab.data('tab-loaded', true);
          $pane.html(frag).trigger("loaded", xhr, $tab.data("list"));
        });
      }
    });
  }

  , ".view-more click" : function(el, ev) {
    var that = this
    , $tab = this.element
              .find(this.options.tab_selector)
              .map(function(i, v) {
                if(that.element.find(get_attr(v, that.options.tab_target_attr)).has(el).length) {
                  return v;
                }
              })
    , view_data = $tab.data("view_data");

    view_data.list.replace(view_data.all_items);
  }


  , "{observer} value" : function(el, ev, newval) {
    this.filter(newval);
    this.element.trigger('kill-all-popovers');
  }

  // @override
  , redo_last_filter : function(id_to_add) {
    var that = this;
    var $tabs = $(this.element).find(this.options.tab_selector);
    var old_sel = this.options.filterable_items_selector;
    var old_ids = this.last_filter_ids;

    $tabs.each(function(i, tab) {
      var $tab = $(tab)
      , model = $tab.data("model")
      , res = old_ids ? that.last_filter.getResultsFor(model) : null
      , view_data = $tab.data("view_data");

      //that.options.filterable_items_selector = $(get_attr($tab, that.options.tab_href_attr)).find("li:not(.view-more, .add-new)");
      that.last_filter_ids = res = res ? can.unique(can.map(res, function(v) { return v.id; })) : null; //null is the show-all case
      if(res) {
        view_data.filtered_items.replace(can.map(view_data.all_items, function(item) { return ~can.inArray(item.id, res) ? item : undefined; }));
      } else {
        view_data.filtered_items.replace(view_data.all_items.slice(0));
      }
      view_data.list.replace(that.options.limit ? view_data.filtered_items.slice(0, that.options.limit) : view_data.filtered_items);

      //that._super();
      // res = can.map(res, function(obj, i) {
      //   var m = new model(obj);
      //   if(!m.selfLink) {
      //     m.refresh();
      //   }
      //   return m;
      // });
      $tab.find(".item-count").html(res ? res.length : $tab.data("view_data").filtered_items.length);
    });
  }

  , ".tabbable loaded" : function(el, ev) {
    $(el).scrollTop(0);
  }

  , ".nav-tabs li click" : function(el, ev) {
    var plural = el.children("a").attr("data-object-plural");
    var singular = can.map(window.cms_singularize(plural).split("_"), can.capitalize).join(" ");
    el.closest(".widget").find(".object-type").text(singular)
      .closest("a").attr("data-object-plural", plural.split(" ").join("_").toLowerCase())
      .attr("data-object-singular", singular.replace(" ", ""));
  }

  , ".show-extended mouseover" : function(el, ev) {
    var $allext = this.element.find(".extended, .show-extended")
    , $extended = el.closest(":has(.extended)").find(".extended:first")
    , instance = el.closest("[data-model]").data("model") || el.closest(":data(model)").data("model");

    if(!$extended.hasClass("in")) {
      $allext.removeClass("in");
      can.view(this.options.tooltip_view, instance, function(frag) {
        this.fade_in_timeout = setTimeout(function() {
          $extended.html(frag).addClass("in").data("model", instance);
          el.addClass("in");
        }, 30);
      });
    }
  }

  , ".show-extended, .extended mouseout" : function(el, ev) {
    var $extended = this.element.find(".extended.in");
    if(!$(ev.relatedTarget).is(".show-extended.in, .extended.in, .show-extended.in *, .extended.in *")) {
      clearTimeout(this.fade_in_timeout);
      el.removeClass("in");
      $extended.removeClass("in");
    }
  }

});

})(this.can, this.can.$);
