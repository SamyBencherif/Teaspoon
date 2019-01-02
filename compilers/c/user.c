
Array u_main() {
  int pool_restore = pool.size;

  b_print(new_array(14,(float[]){72, 101, 108, 108, 111, 44, 32, 87, 111, 114, 108, 100, 10, 0}));

  Array ret_0 = new_array(0, (float[]){});
  reset_pool(ret_0.get, pool_restore);
  return ret_0;

  Array ret_1 = new_array(0, (float[]){});
  reset_pool(ret_1.get, pool_restore);
  return ret_1;
}
