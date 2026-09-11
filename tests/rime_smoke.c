/* MIT. Run against a scratch user directory; never the user's live Rime data. */
#include <stdio.h>
#include <string.h>
#include <rime_api.h>

int main(int argc, char **argv) {
  if (argc != 8) {
    fprintf(stderr, "usage: smoke user shared staging logs schema keys expected\n");
    return 2;
  }
  RimeApi *api = rime_get_api();
  RIME_STRUCT(RimeTraits, traits);
  traits.user_data_dir = argv[1];
  traits.shared_data_dir = argv[2];
  traits.staging_dir = argv[3];
  traits.prebuilt_data_dir = argv[3];
  traits.log_dir = argv[4];
  traits.app_name = "rime.openlegallexicon-test";
  traits.min_log_level = 2;
  api->setup(&traits);
  api->initialize(&traits);
  RimeSessionId session = api->create_session();
  int found = 0;
  if (session && api->select_schema(session, argv[5]) && api->simulate_key_sequence(session, argv[6])) {
    RIME_STRUCT(RimeContext, context);
    if (api->get_context(session, &context)) {
      for (int i = 0; i < context.menu.num_candidates; ++i) {
        printf("candidate: %s\n", context.menu.candidates[i].text);
        if (strcmp(context.menu.candidates[i].text, argv[7]) == 0) found = 1;
      }
      api->free_context(&context);
    }
  }
  if (RIME_API_AVAILABLE(api, get_version)) printf("librime: %s\n", api->get_version());
  if (session) api->destroy_session(session);
  api->finalize();
  if (!found) fprintf(stderr, "expected candidate was not found: %s\n", argv[7]);
  return found ? 0 : 1;
}
