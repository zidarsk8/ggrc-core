import * as businessModels from './business-models';
import * as serviceModels from './service-models';
import * as mappingModels from './mapping-models';

export default {
  ...businessModels,
  ...serviceModels,
  ...mappingModels,
};
