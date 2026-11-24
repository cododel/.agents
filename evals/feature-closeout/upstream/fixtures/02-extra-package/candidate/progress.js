import lodash from 'lodash';
export const normalize = (value) => lodash.clamp(value, 0, 100);
