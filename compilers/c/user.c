
Array u_hello(Array r) {
  int pool_restore = pool.size;

  Array v_x=new_array(4,(float[]){5, 6, 7, 8});
  Array v_y=new_array(4,(float[]){8, 6, 7, 8});
  Array v_z=new_array(4,(float[]){99, 6, 7, 8});

  Array ret_0 = new_array(6,(float[]){78, 105, 99, 101, 33, 10});
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
  Array v_x=new_array(1, (float[]){0});
  while(b_less(v_x, new_array(1, (float[]){5})).get[0]){
    b_print(u_hello(v_r));
    b_print(b_sum(new_array(2,(float[]){65, b_mul(new_array(2,(float[]){v_x.get[0], 10}))})));
    v_		print("\n");
    v_x=b_sum(v_x, new_array(1, (float[]){1}));
  }

  Array ret_4 = new_array(0, (float[]){});
  reset_pool(ret_4.get, pool_restore);
  return ret_4;
}
