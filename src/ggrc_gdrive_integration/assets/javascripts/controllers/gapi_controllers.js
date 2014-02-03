;(function(CMS, GGRC, can, $) {

  GGRC.Controllers.Modals("GGRC.Controllers.GAPIModal", {
    defaults: {
      skip_refresh: true
      , content_view : GGRC.mustache_path + "/gdrive/auth_button.mustache"
    }
    , init : function() {
      this._super.apply(this, arguments);
      this.defaults.button_view = can.view.mustache("");
    }
  }, {
    init : function() {
      this._super();
      this.element.trigger("shown");
    }

    , "{scopes} change" : function() {
      this.element.trigger("shown");
    }

    , "{$content} a.btn[data-toggle=gapi] click" : function(el, ev) {
      GGRC.Controllers.GAPI.doGAuth_step2(null, true);
      window.oauth_dfd.always($.proxy(this.element, "modal_form", "hide"));
    }

  });

  window.oauth_dfd = new $.Deferred();

  can.Control("GGRC.Controllers.GAPI", {
    canonical_instance : null
    , o2dfd : null
    , drivedfd : null
    , gapidfd : new $.Deferred()
  
    , authorize : function(newscopes) {
      return this.canonical_instance.authorize(newscopes);
    }

    , doGAuth : function(scopes, use_popup) {
      var that = this;
      this.drive = this.drive || new $.Deferred();
      if(window.oauth_dfd.state() !== "pending") {
        window.oauth_dfd = new $.Deferred();
      }
      can.each({
        "drivedfd" : "drive"
        , "o2dfd" : "oauth2"
      }, function(p, d) {
        if(!that[d]) {
          that[d] = new $.Deferred();
          that.gapidfd.done(function() {
            window.gapi.client.load(p, 'v2', function(result) {
              if(!result){
                that[d].resolve();
              } else {
                that[d].reject(result);
              }
            });
          });
        }
      });

      if(use_popup) {
        if(!$(".ggrc_controllers_gapi.modal").length) {
          $("<div class='modal hide'>").modal_form().appendTo(document.body).ggrc_controllers_gapi_modal({
            scopes : scopes
            , modal_title : "Please log in to Google API"
            , new_object_form : true
          });
        }
      } else {
        this.doGAuth_step2(scopes, use_popup);
      }
    }
    , doGAuth_step2 : function(scopes, use_popup) {
      var authdfd = new $.Deferred()
      , that = this;

      scopes = scopes || this.canonical_instance.options.scopes;

      this.gapidfd.done(function() {
        window.gapi.auth.authorize({
          'client_id': GGRC.config.GAPI_CLIENT_ID
          , 'scope': scopes.serialize()
          , 'immediate': !use_popup
          , 'login_hint' : GGRC.current_user && GGRC.current_user.email
        }).then(function(authresult) {
          authdfd.resolve(authresult);
        }, function() {
          if(!use_popup) {
            that.doGAuth(scopes, true);
            authdfd.reject("login required. Switching to non-immediate");
          } else {
            window.oauth_dfd.reject();
            authdfd.reject("auth failed");
          }
        });
      });
      $.when(authdfd, this.o2dfd)
      .then(function(authresult) {
        var o2d = new $.Deferred();
        gapi.client.oauth2.userinfo.get().execute(function(user) {
          if(user.error) {
            $(document.body.trigger("ajax:flash", { error : user.error }));
            o2d.reject(user.error);
          } else {
            o2d.resolve(user);
          }
        });
        return $.when(authresult, o2d);
      })
      .done(function(authresult, o2result){  //success
        if(!authresult)
          return; //assume we had to do a non-immediate auth

        if(o2result.email.toLowerCase().trim() !== GGRC.current_user.email.toLowerCase().trim()) {
          $(document.body).trigger(
            "ajax:flash"
            , { warning : [
              "You are signed into GGRC as"
              , GGRC.current_user.email
              , "and into Google Apps as"
              , o2result.email
              , ". You may experience problems uploading evidence."
              ].join(' ')
            });
        }
        oauth_dfd.resolve(authresult, o2result);
      });
    }
    , gapi_request_with_auth : function(params) {
      var that = this;
      return that.authorize(params.scopes).then(function() {
        var dfd = new $.Deferred();
        var cb = params.callback;
        var check_auth = function(result) {
          var args = can.makeArray(arguments);
          args.unshift(dfd);
          if(result && result.error && result.error.code === 401) {
            that.doGAuth(scopes); //changes oauth_dfd to a new deferred
            params.callback = cb;
            that.authorize(params.scopes).then($.proxy(gapi_request_with_auth, that, params))
            .then(
              function() {
                dfd.resolve.apply(dfd, arguments);
              }, function() {
                dfd.reject.apply(dfd, arguments);
              });
          } else {
            cb.apply(window, args);
          }
        };
        params.callback = check_auth;
        if(typeof params.path === "function") {
          params.path = params.path();
        }
        window.gapi.client.request(params);
        return dfd.promise();
      });
    }

  }, {

    init : function() {
      this._super.apply(this, arguments);
      if(!this.constructor.canonical_instance) {
        this.constructor.canonical_instance = this;
      }
      if(this.options.scopes.length) {
        this.constructor.doGAuth(this.options.scopes);
      }

      this.doGAuthWithScopes = $.proxy(this.constructor, "doGAuth", this.options.scopes);
    }

    , authorize : function(newscopes) {
      var that = this;
      can.each(newscopes, function(ns) {
        if(!~can.inArray(ns, that.options.scopes)) {
          that.options.scopes.push(ns);
        }
      });
      return window.oauth_dfd;
    }

    , "{scopes} change" : function(scopes, ev) {
      can.debounce(500, this.doGAuthWithScopes); //debounce in case we push several scopes in sequence
    }
  });

})(this.CMS, this.GGRC, this.can, this.can.$);
