
Array u_main() {
  int pool_restore = pool.size;

  Array v_x=new_array(0,(float[]){});
  b_push(&v_x, new_array(1, (float[]){65}));
  b_push(&v_x, new_array(1, (float[]){66}));
  b_print(v_x);

  Array ret_0 = new_array(0, (float[]){});
  reset_pool(ret_0.get, pool_restore);
  return ret_0;
}
