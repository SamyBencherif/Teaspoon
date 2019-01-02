
/**
Teaspoon Compatability Layer
Samy Bencherif (2018)
*/

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>

struct array {
  int len;
  float* get;
};

typedef struct array Array;

typedef struct LLNode LLNode;

struct LLNode
{
  Array data;
  LLNode* next;
};

struct LinkedList
{
  LLNode* head;
  int size;
};

typedef struct LinkedList alloc_mgr;

alloc_mgr pool;

// push tracker
void track_allocation(Array arr)
{
  if (pool.size == 0)
  {
    LLNode* head = malloc(sizeof(LLNode));
    // printf("[ALLOC] Tracker Node\n");
    pool.head = head;
    pool.head->data = arr;
  } else
  {
    LLNode* tmp = pool.head;
    LLNode* head = malloc(sizeof(LLNode));
    // printf("[ALLOC] Tracker Node\n");
    pool.head = head;
    pool.head->data = arr;
    pool.head->next = tmp;
  }
  pool.size++;
  // printf("Tracked %i allocations.\n", pool.size);
}

void free_array(Array arr)
{
  int size = arr.len;
  // printf("[FREE] %lu bytes for an %d element array.\n", size*sizeof(float)+sizeof(size), size);
  free(arr.get);
}

// free array and tracker
void pop_from_pool()
{
  if (pool.size > 0)
  {
    LLNode* tmp = pool.head;
    free_array(pool.head->data);
    pool.head = pool.head->next;
    free(tmp);
    // printf("[FREE] Tracker Node\n");
    pool.size--;
  } else
  {
    printf("TCL freed unallocated memory.\n");
    exit(1);
  }
}

// free tracker only
void discard_from_pool()
{
  if (pool.size > 0)
  {
    LLNode* tmp = pool.head;
    pool.head = pool.head->next;
    free(tmp);
    // printf("[FREE] Tracker Node\n");
    pool.size--;
  } else
  {
    printf("TCL freed unallocated memory.\n");
    exit(1);
  }
}

// pop many
void reset_pool(float* excludes, int pool_restore)
{
  Array tmp;
  bool wasExclude = false; //deletion of last element is skipped without comparison.
  while (pool.size > pool_restore) //save one variable to return
  {
    if (pool.head->data.get != excludes)
    {
      pop_from_pool();
    } else {
      tmp = pool.head->data;
      discard_from_pool();
      wasExclude = true;
    }
  }

  if (wasExclude)
  {
    track_allocation(tmp);
  }
}

Array new_array(int l, float* v)
{
  Array o;
  o.len = l;

  // printf("[ALLOC] %lu bytes for an %d element array.\n", l*sizeof(float)+sizeof(l), l);
  float* arr = malloc(l*sizeof(float));
  for(int i=0; i<l; i++)
    arr[i] = v[i];

  o.get = arr;

  track_allocation(o);

  return o;
}

/** Standard Library */
#include "stdlib.c"
/** End Standard Library */

#include "extensions.c"

/** User Code */
#include "user.c"
/** End User Code */

int main(void)
{

  int pool_restore = pool.size;  // expected to be 0.
  u_main();
  reset_pool(NULL, pool_restore);

  if (pool.size > 0)
  {
    printf("Memory Leak Detected. %i unresolved objects. \n", pool.size);
  }
  return pool.size;
}