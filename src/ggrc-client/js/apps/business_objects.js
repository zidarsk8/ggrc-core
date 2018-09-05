/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import SummaryWidgetController from '../controllers/summary_widget_controller';
import DashboardWidget from '../controllers/dashboard_widget_controller';
import InfoWidget from '../controllers/info_widget_controller';
import WidgetList from '../modules/widget_list';
import {isDashboardEnabled} from '../plugins/utils/dashboards-utils';
import {
  getWidgetConfig,
} from '../plugins/utils/object-versions-utils';
import {widgetModules} from '../plugins/utils/widgets-utils';
import {
  getPageInstance,
  getPageModel,
} from '../plugins/utils/current-page-utils';
import * as businessModels from '../models/business-models/index';
import TreeViewConfig from '../apps/base_widgets';

let CoreExtension = {};

CoreExtension.name = 'core"';
widgetModules.push(CoreExtension);
_.assign(CoreExtension, {
  init_widgets: function () {
    let baseWidgetsByType = TreeViewConfig.attr('base_widgets_by_type');
    let widgetList = new WidgetList('ggrc_core');
    let objectClass = getPageModel();
    let objectTable = objectClass && objectClass.table_plural;
    let object = getPageInstance();
    let path = GGRC.mustache_path;
    let infoWidgetViews;
    let summaryWidgetViews;
    let modelNames;
    let possibleModelType;
    let farModels;
    let extraDescriptorOptions;
    let extraContentOptions;

    // Info and summary widgets display the object information instead of listing
    // connected objects.
    summaryWidgetViews = {
      audits: path + '/audits/summary.mustache',
    };
    if (summaryWidgetViews[objectTable]) {
      widgetList.add_widget(object.constructor.shortName, 'summary', {
        widget_id: 'summary',
        content_controller: SummaryWidgetController,
        instance: object,
        widget_view: summaryWidgetViews[objectTable],
        order: 3,
        uncountable: true,
      });
    }
    if (isDashboardEnabled(object)) {
      widgetList.add_widget(object.constructor.shortName, 'dashboard', {
        widget_id: 'dashboard',
        content_controller: DashboardWidget,
        instance: object,
        widget_view: path + '/base_objects/dashboard_widget.mustache',
        order: 6,
        uncountable: true,
      });
    }
    infoWidgetViews = {
      programs: path + '/programs/info.mustache',
      audits: path + '/audits/info.mustache',
      people: path + '/people/info.mustache',
      policies: path + '/policies/info.mustache',
      controls: path + '/controls/info.mustache',
      systems: path + '/systems/info.mustache',
      processes: path + '/processes/info.mustache',
      products: path + '/products/info.mustache',
      assessments: path + '/assessments/info.mustache',
      assessment_templates:
        path + '/assessment_templates/info.mustache',
      issues: path + '/issues/info.mustache',
      evidence: path + '/evidence/info.mustache',
      documents: path + '/documents/info.mustache',
      risks: path + '/risks/info.mustache',
    };
    widgetList.add_widget(object.constructor.shortName, 'info', {
      widget_id: 'info',
      content_controller: InfoWidget,
      instance: object,
      widget_view: infoWidgetViews[objectTable],
      order: 5,
      uncountable: true,
    });
    modelNames = can.Map.keys(baseWidgetsByType);
    modelNames.sort();
    possibleModelType = modelNames.slice();
    can.each(modelNames, function (name) {
      let wList;
      let childModelList = [];
      let widgetConfig = getWidgetConfig(name);
      name = widgetConfig.name;
      TreeViewConfig.attr('basic_model_list').push({
        model_name: name,
        display_name: widgetConfig.widgetName,
      });

      // Initialize child_model_list, and child_display_list each model_type
      wList = baseWidgetsByType[name];

      can.each(wList, function (item) {
        let childConfig;
        if (possibleModelType.indexOf(item) !== -1) {
          childConfig = getWidgetConfig(name);
          childModelList.push({
            model_name: childConfig.name,
            display_name: childConfig.widgetName,
          });
        }
      });
      TreeViewConfig.attr('sub_tree_for').attr(name, {
        model_list: childModelList,
        display_list: businessModels[name]
          .tree_view_options.child_tree_display_list || wList,
      });
    });

    function applyMixins(definitions) {
      let mappings = {};

      // Recursively handle mixins
      function reifyMixins(definition) {
        let finalDefinition = {};
        if (definition._mixins) {
          can.each(definition._mixins, function (mixin) {
            if (typeof (mixin) === 'string') {
              // If string, recursive lookup
              if (!definitions[mixin]) {
                console.warn(`Undefined mixin: ${mixin} ${definitions}`);
              } else {
                can.extend(
                  finalDefinition,
                  reifyMixins(definitions[mixin])
                );
              }
            } else if (can.isFunction(mixin)) {
              // If function, call with current definition state
              mixin(finalDefinition);
            } else {
              // Otherwise, assume object and extend
              can.extend(finalDefinition, mixin);
            }
          });
        }
        can.extend(finalDefinition, definition);
        delete finalDefinition._mixins;
        return finalDefinition;
      }

      can.each(definitions, function (definition, name) {
        // Only output the mappings if it's a model, e.g., uppercase first letter
        if (name[0] === name[0].toUpperCase()) {
          mappings[name] = reifyMixins(definition);
        }
      });

      return mappings;
    }

    // the assessments_view only needs the Assessments widget
    if (/^\/assessments_view/.test(window.location.pathname)) {
      farModels = ['Assessment'];
    } else {
      farModels = baseWidgetsByType[object.constructor.shortName];
    }

    // here we are going to define extra descriptor options, meaning that
    //  these will be used as extra options to create widgets on top of

    extraDescriptorOptions = {
      all: (function () {
        let all = {
          Evidence: {
            treeViewDepth: 0,
          },
          AssessmentTemplate: {
            treeViewDepth: 0,
          },
        };

        let defOrder = TreeViewConfig.attr('defaultOrderTypes');
        Object.keys(defOrder).forEach(function (type) {
          if (!all[type]) {
            all[type] = {};
          }
          all[type].order = defOrder[type];
        });

        return all;
      })(),

      // An Audit has a different set of object that are more relevant to it,
      // thus these objects have a customized priority. On the other hand,
      // the object otherwise prioritized by default (e.g. Regulation) have
      // their priority lowered so that they fit nicely into the alphabetical
      // order among the non-prioritized object types.
      Audit: {
        Assessment: {
          order: 7,
        },
        Issue: {
          order: 8,
        },
        Evidence: {
          order: 9,
        },
      },
    };

    extraContentOptions = applyMixins({
      business_objects: {
        Audit: {
          add_item_view: path + '/audits/tree_add_item.mustache',
        },
      },
      Program: {
        _mixins: [
          'business_objects',
        ],
        Person: {
          allow_creating: true,
        },
      },
      Audit: {
        _mixins: ['business_objects'],
        Program: {
          allow_creating: false,
        },
        Assessment: {
          add_item_view: path + '/assessments/tree_add_item.mustache',
        },
        AssessmentTemplate: {
          add_item_view: GGRC.mustache_path +
            '/assessment_templates/tree_add_item.mustache',
        },
        Person: {
          content_controller_options: {
            allow_creating: false,
          },
        },
      },
      Regulation: {
        _mixins: ['business_objects'],
      },
      Standard: {
        _mixins: ['business_objects'],
      },
      Policy: {
        _mixins: ['business_objects'],
      },
      Contract: {
        _mixins: ['business_objects'],
      },
      Requirement: {
        _mixins: ['business_objects'],
      },
      Objective: {
        _mixins: ['business_objects'],
      },
      Control: {
        _mixins: ['business_objects'],
      },
      Assessment: {
        _mixins: ['business_objects'],
        Audit: {
          allow_creating: false,
          add_item_view: path + '/audits/tree_add_item.mustache',
        },
      },
      AssessmentTemplate: {
        Audit: {
          allow_creating: false,
        },
      },
      Risk: {
        _mixins: ['business_objects'],
      },
      Threat: {
        _mixins: ['business_objects'],
      },
      Issue: {
        _mixins: ['business_objects'],
      },
      AccessGroup: {
        _mixins: ['business_objects'],
      },
      DataAsset: {
        _mixins: ['business_objects'],
      },
      Facility: {
        _mixins: ['business_objects'],
      },
      Market: {
        _mixins: ['business_objects'],
      },
      Metric: {
        _mixins: ['business_objects'],
      },
      OrgGroup: {
        _mixins: ['business_objects'],
      },
      Vendor: {
        _mixins: ['business_objects'],
      },
      Process: {
        _mixins: ['business_objects'],
      },
      Product: {
        _mixins: ['business_objects'],
      },
      ProductGroup: {
        _mixins: ['business_objects'],
      },
      Project: {
        _mixins: ['business_objects'],
      },
      System: {
        _mixins: ['business_objects'],
      },
      TechnologyEnvironment: {
        _mixins: ['business_objects'],
      },
    });

    // Disable editing on profile pages, as long as it isn't audits on the dashboard
    if (getPageInstance() instanceof businessModels.Person) {
      let personOptions = extraContentOptions.Person;
      can.each(personOptions, function (options, modelName) {
        if (modelName !== 'Audit' || !/dashboard/.test(window.location)) {
          can.extend(options, {
            allow_creating: false,
          });
        }
      });
    }

    can.each(farModels, function (modelName) {
      let widgetConfig = getWidgetConfig(modelName);
      modelName = widgetConfig.name;

      let farModel;
      let descriptor = {};
      let widgetId;

      farModel = businessModels[modelName];
      if (farModel) {
        widgetId = widgetConfig.widgetId;
        descriptor = {
          instance: object,
          far_model: farModel,
        };
      } else {
        widgetId = modelName;
      }

      // Custom overrides
      if (extraDescriptorOptions.all &&
          extraDescriptorOptions.all[modelName]) {
        $.extend(descriptor, extraDescriptorOptions.all[modelName]);
      }

      if (extraDescriptorOptions[object.constructor.shortName] &&
          extraDescriptorOptions[object.constructor.shortName][modelName]) {
        $.extend(descriptor,
          extraDescriptorOptions[object.constructor.shortName][modelName]);
      }

      if (extraContentOptions[object.constructor.shortName] &&
          extraContentOptions[object.constructor.shortName][modelName]) {
        $.extend(true, descriptor, {
          content_controller_options:
          extraContentOptions[object.constructor.shortName][modelName],
        });
      }
      descriptor.widgetType = 'treeview';
      widgetList.add_widget(
        object.constructor.shortName, widgetId, descriptor);
    });
  },
});
