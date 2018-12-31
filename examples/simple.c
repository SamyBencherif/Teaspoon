
Array u_hello() {
  int pool_restore = pool.size;

  Array v_x=new_array(4,(float[]){5, 6, 7, 8});
  Array v_y=new_array(4,(float[]){8, 6, 7, 8});
  Array v_z=new_array(4,(float[]){99, 6, 7, 8});

  Array ret_0 = new_array(4,(float[]){70, 68, 80, 91});
  reset_pool(ret_0.get, pool_restore);
  return ret_0;

  Array ret_1 = new_array(0, (float[]){});
  reset_pool(ret_1.get, pool_restore);
  return ret_1;
}

Array u_world() {
  int pool_restore = pool.size;

  Array v_x=new_array(4,(float[]){5, 6, 7, 8});
  Array v_y=new_array(4,(float[]){8, 6, 7, 8});
  Array v_z=new_array(4,(float[]){99, 6, 7, 8});

  Array ret_2 = v_x;
  reset_pool(ret_2.get, pool_restore);
  return ret_2;

  Array ret_3 = new_array(0, (float[]){});
  reset_pool(ret_3.get, pool_restore);
  return ret_3;
}

Array u_main() {
  int pool_restore = pool.size;

  Array v_r=new_array(4,(float[]){7, 7, 7, 7});
  b_print(u_hello());

  Array ret_4 = new_array(0, (float[]){});
  reset_pool(ret_4.get, pool_restore);
  return ret_4;
}

