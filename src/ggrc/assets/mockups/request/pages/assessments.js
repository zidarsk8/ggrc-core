(function (GGRC, Generator) {
  GGRC.Bootstrap.Mockups = GGRC.Bootstrap.Mockups || {};
  GGRC.Bootstrap.Mockups.Request = GGRC.Bootstrap.Mockups.Request || {};

  GGRC.Bootstrap.Mockups.Request.Assessments = {
    title: "Assessments",
    icon: "assessment",
    template: "/request/widget.mustache",
    children: GGRC.Bootstrap.Mockups.Assessor.Assessments.children
  };
})(GGRC || {}, GGRC.Mockup.Generator);
