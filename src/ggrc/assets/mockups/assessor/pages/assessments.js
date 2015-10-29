(function (GGRC, Generator) {
  GGRC.Bootstrap.Mockups = GGRC.Bootstrap.Mockups || {};
  GGRC.Bootstrap.Mockups.Assessor = GGRC.Bootstrap.Mockups.Assessor || {};

  GGRC.Bootstrap.Mockups.Assessor.Assessments = {
    title: "Assessments",
    icon: "grcicon-assessment-color",
    template: "/assessor/assessments.mustache",
    hide_filter: true,
    children: Generator.get("assessment", 3)
  };
})(GGRC || {}, GGRC.Mockup.Generator);
