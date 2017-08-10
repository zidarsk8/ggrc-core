/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (can, GGRC, $) {
  'use strict';

  var AUTO_SAVE_DELAY = 1000;
  var CA_DD_REQUIRED_DEPS =
    GGRC.Utils.CustomAttributes.CA_DD_REQUIRED_DEPS;

  // helper functions
  function addToSet(arr, value) {
    var idx = arr.indexOf(value);
    if (idx === -1) {
      arr.push(value);
    }
  }

  function removeFromSet(arr, value) {
    var idx = arr.indexOf(value);
    if (idx > -1) {
      arr.splice(idx, 1);
    }
  }

  GGRC.Components('autoSaveForm', {
    tag: 'auto-save-form',
    template: can.view(
      GGRC.mustache_path +
      '/components/auto-save-form/auto-save-form.mustache'
    ),
    viewModel: {
      _fields: new can.List([]),
      define: {
        fieldsToSave: {
          Value: can.Map
        },
        isDirty: {
          type: 'boolean',
          get: function () {
            return can.Map.keys(this.attr('fieldsToSave') || {}).length;
          }
        },
        hasValidationErrors: {
          type: 'boolean',
          get: function () {
            return this.attr('fields')
              .filter(function (field) {
                return !field.attr('validation.valid');
              }).length;
          }
        },
        evidenceAmount: {
          type: 'number',
          set: function (newValue, setValue) {
            setValue(newValue);
            this.updateEvidenceValidation();
          }
        },
        notEnoughEvidences: {
          /**
           * Checks if there's enough evidences to pass validation
           * @return {Boolean} has missing evidences
           */
          get: function () {
            var optionsWithEvidence = this.attr('fields')
                  .filter(function (item) {
                    return item.attr('type') === 'dropdown';
                  })
                  .filter(function (item) {
                    var requiredOption =
                      item.attr('validationConfig')[item.attr('value')];

                    return requiredOption === CA_DD_REQUIRED_DEPS.EVIDENCE ||
                       requiredOption ===
                        CA_DD_REQUIRED_DEPS.COMMENT_AND_EVIDENCE;
                  }).length;
            return optionsWithEvidence > this.attr('evidenceAmount');
          }
        },
        // update only the fields which values are updated
        // this helps canJS to update only those components which need to be
        // updated
        fields: {
          get: function () {
            return this.attr('_fields');
          },
          set: function (newFields) {
            var fields = this.attr('_fields');

            if (!fields.length) {
              this.attr('_fields', newFields);
              return;
            }

            newFields.forEach(function (nf) {
              var oldField = null;
              var valuesEqual;
              var validationEqual;

              fields.forEach(function (field) {
                if (field.id === nf.id) {
                  oldField = field;
                }
              });
              if (oldField) {
                valuesEqual = oldField.value === nf.value;
                validationEqual =
                  _.isEqual(oldField.validation.attr(), nf.validation.attr());

                if (!valuesEqual || !validationEqual) {
                  oldField.attr(nf);
                }
              }
            });
            this.attr('_fields', fields);
          }
        }
      },
      formSavedDeferred: can.Deferred().resolve(),
      editMode: false,
      saving: false,
      allSaved: true,
      fieldsToSaveAvailable: false,
      autoSaveScheduled: false,
      autoSaveAfterSave: false,
      autoSaveTimeoutHandler: null,
      fields: [],
      saveCallback: null,
      triggerSaveCbs: null,
      init: function () {
        this._save = this.save.bind(this);
        this.attr('triggerSaveCbs').add(this._save);
      },
      unsubscribe: function () {
        this.attr('triggerSaveCbs').remove(this._save);
      },

      // part of latency compensation. reflects evidence changes
      updateEvidenceValidation: function () {
        var notEnoughEvidences = this.attr('notEnoughEvidences');
        this.attr('fields')
          .filter(function (field) {
            return field.attr('type') === 'dropdown';
          })
          .each(function (field) {
            var valCfg = field.validationConfig;
            var fieldValidationConf = valCfg && valCfg[field.value];
            var errors = field.attr('preconditions_failed') || [];
            var evidenceRequired =
              fieldValidationConf === CA_DD_REQUIRED_DEPS.EVIDENCE ||
              fieldValidationConf === CA_DD_REQUIRED_DEPS.COMMENT_AND_EVIDENCE;

            if (notEnoughEvidences) {
              if (evidenceRequired) {
                addToSet(errors, 'evidence');
              }
            } else {
              removeFromSet(errors, 'evidence');
            }
            field.attr('preconditions_failed', errors);
            this.performValidation(field, field.value, true);
          }.bind(this));
      },

      hasMissingComment: function (field, value) {
        return field.attr('errorsMap.comment');
      },
      hasMissingEvidence: function (field) {
        var requiredOption =
          field.attr('validationConfig')[field.attr('value')];

        return requiredOption === CA_DD_REQUIRED_DEPS.EVIDENCE ||
           requiredOption === CA_DD_REQUIRED_DEPS.COMMENT_AND_EVIDENCE;
      },

      // instantly reflects changes to the document
      // to compensate for network latency
      networkLatencyCompensation: function (field, value) {
        var valCfg = field.validationConfig;
        var fieldValidationConf = valCfg && valCfg[value];
        var errors = field.attr('preconditions_failed') || [];

        var requiresComment =
          fieldValidationConf === CA_DD_REQUIRED_DEPS.COMMENT ||
          fieldValidationConf === CA_DD_REQUIRED_DEPS.COMMENT_AND_EVIDENCE;

        if (field.attr('type') === 'dropdown') {
          if (requiresComment) {
            addToSet(errors, 'comment');
          } else {
            removeFromSet(errors, 'comment');
          }

          field.attr('preconditions_failed', errors);
        }

        if (errors.indexOf('value') > -1 && value) {
          removeFromSet(errors, 'value');
          field.attr('preconditions_failed', errors);
        }

        this.updateEvidenceValidation();
      },

      /**
       * Performs validation of the changed field
       * @param  {Object}  field                    field or custom attribute object
       * @param  {Any}     value                    new value
       * @param  {Boolean} isAllEvidencesValidation is validation called for all
       *                                            evidence required fields in
       *                                            a loop
       */
      performValidation: function (field, value, isAllEvidencesValidation) {
        var plainFieldObj = field.attr();

        var valResult = GGRC.Utils.CustomAttributes
          .validateField(plainFieldObj, value);

        if (!isAllEvidencesValidation && valResult.validation.hasMissingInfo) {
          this.dispatch({
            type: 'validationChanged',
            field: field
          });
        }

        field.attr(valResult);
      },
      fieldValueChanged: function (e, field) {
        field.attr('value', e.value);
        this.fieldsToSave.attr(e.fieldId, e.value);
        this.attr('fieldsToSaveAvailable', true);

        this.networkLatencyCompensation(field, e.value);
        this.performValidation(field, e.value);

        this.attr('formSavedDeferred', can.Deferred());
        this.triggerAutoSave();
      },
      save: function () {
        var self = this;
        var toSave = {};

        this.attr('fieldsToSave').each(function (v, k) {
          toSave[k] = v;
        });

        this.attr('fieldsToSave', {}, true);
        this.attr('fieldsToSaveAvailable', false);

        clearTimeout(this.attr('autoSaveTimeoutHandler'));
        this.attr('autoSaveScheduled', false);

        this.attr('saving', true);
        this.saveCallback(new can.Map(toSave))
          .done(function () {
            if (self.attr('autoSaveAfterSave')) {
              self.attr('autoSaveAfterSave', false);
              setTimeout(self.save.bind(self));
            }

            self.attr('allSaved', true);
            self.attr('formSavedDeferred').resolve();
          })
          // fix: error handling
          .always(function () {
            self.attr('saving', false);
          });
      },
      triggerAutoSave: function () {
        if (this.attr('autoSaveScheduled')) {
          return;
        }
        if (this.attr('saving')) {
          this.attr('autoSaveAfterSave', true);
          return;
        }

        this.attr('allSaved', false);

        this.attr(
          'autoSaveTimeoutHandler',
          setTimeout(this.save.bind(this), AUTO_SAVE_DELAY)
        );
        this.attr('autoSaveScheduled', true);
      }
    },
    events: {
      removed: function () {
        this.viewModel.unsubscribe();
      }
    }
  });
})(window.can, window.GGRC, window.jQuery);
