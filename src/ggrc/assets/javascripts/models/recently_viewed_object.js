can.Model.LocalStorage("GGRC.Models.RecentlyViewedObject", {

  newInstance : function(attrs) {
    if(attrs instanceof can.Model) {
      return new this({
        type : attrs.constructor.shortName
        , model : attrs.constructor
        , viewLink : attrs.viewLink
        , title : attrs.title
      });
    } else {
      return this._super(attrs);
    }
  }

}, {

  init : function() {
    this.attr("model", GGRC.Models[this.type] || CMS.Models[this.type]);
  }

  , stub : function() {
    return can.extend(this._super(), { title : this.title, viewLink : this.viewLink });
  }
});